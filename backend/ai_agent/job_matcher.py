from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import tool
from scripts.job_search import JobSearchAPI
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    warnings.warn("OPENAI_API_KEY not found in environment variables. Some features may be limited.")
    os.environ["OPENAI_API_KEY"] = "dummy_key"  # Set a dummy key for development

class JobMatcher:
    def __init__(self):
        self.job_search_api = JobSearchAPI()
        self.conversation_history = []
        try:
            self.llm = ChatOpenAI(temperature=0)
        except Exception as e:
            print(f"Warning: Could not initialize ChatOpenAI: {e}")
            self.llm = None
    
    def add_to_conversation(self, message: str, sender: str = 'user'):
        """Add a message to conversation history"""
        self.conversation_history.append({
            'text': message,
            'sender': sender,
            'timestamp': datetime.now().isoformat()
        })

    @tool
    def search_jobs(self, query: str) -> dict:
        """Search jobs based on conversation context and current query"""
        # Add current query to conversation
        self.add_to_conversation(query)
        
        # Extract job parameters from conversation history
        params = self.job_search_api.extract_job_params(self.conversation_history)
        
        # Run async job search in sync context
        loop = asyncio.get_event_loop()
        job_results = loop.run_until_complete(
            self.job_search_api.search_all(query, params=params)
        )
        
        if job_results["status"] == "success" and job_results["jobs"]:
            # Get top 3 jobs
            top_matches = []
            for job in job_results["jobs"][:3]:
                formatted_job = self.job_search_api.format_job_for_chat(job)
                top_matches.append({
                    "job": job,
                    "formatted": formatted_job
                })
            
            return {
                "status": "success",
                "matches": top_matches,
                "search_params": params,
                "total_results": len(job_results["jobs"]),
                "message": self._generate_response_message(params, top_matches)
            }
        
        return {
            "status": "error",
            "message": "No matching jobs found",
            "search_params": params
        }

    def _generate_response_message(self, params: dict, matches: list) -> str:
        """Generate a natural language response about the job matches"""
        response = "Based on our conversation, I found these relevant positions:\n\n"
        
        # Add search criteria
        response += "Search criteria:\n"
        if params.get('title'):
            response += f"- Position: {params['title']}\n"
        if params.get('location'):
            response += f"- Location: {params['location']}\n"
        if params.get('salary'):
            response += f"- Salary: {params['salary']}\n"
        if params.get('type'):
            response += f"- Type: {params['type']}\n"
        if params.get('experience'):
            response += f"- Experience: {params['experience']}\n"
        
        response += "\nTop matches:\n"
        for match in matches:
            response += match["formatted"] + "\n"
        
        return response

    @tool
    def refine_search(self, feedback: str) -> dict:
        """Refine job search based on user feedback"""
        self.add_to_conversation(feedback)
        return self.search_jobs(feedback)

def build_agent():
    matcher = JobMatcher()
    tools = [matcher.search_jobs, matcher.refine_search]
    return initialize_agent(
        tools, 
        matcher.llm, 
        agent="conversational-react-description", 
        verbose=True
    )
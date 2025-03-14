from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import tool
from scripts.job_search import JobSearchAPI
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import warnings
import aiohttp
from langchain_ollama import OllamaLLM
import json
from pydantic import BaseModel, Field
from utils.logger import get_logger

# Set up logger for this module
logger = get_logger('job_matcher')

# Load environment variables
load_dotenv()

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    warnings.warn("OPENAI_API_KEY not found in environment variables. Some features may be limited.")
    os.environ["OPENAI_API_KEY"] = "dummy_key"  # Set a dummy key for development

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query string")

class JobMatcher:
    def __init__(self, use_ollama=True):
        self.job_search_api = JobSearchAPI()
        self.conversation_history = []
        try:
            if use_ollama:
                logger.debug("Initializing Ollama LLM")
                self.llm = OllamaLLM(model="llama2")
            else:
                logger.debug("Initializing OpenAI LLM")
                if not os.getenv("OPENAI_API_KEY"):
                    raise ValueError("OPENAI_API_KEY not found in environment variables")
                self.llm = ChatOpenAI(temperature=0)
        except Exception as e:
            logger.warning(f"Could not initialize LLM: {e}")
            self.llm = None
        
        # Initialize tools after everything else is set up
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize and bind the tool methods to the instance"""
        logger.debug("Initializing tools...")
        try:
            # Create bound method instances
            search_jobs_bound = self._search_jobs_impl.__get__(self, JobMatcher)
            refine_search_bound = self._refine_search_impl.__get__(self, JobMatcher)
            
            # Create tools with bound methods
            self.search_jobs_tool = tool(
                args_schema=SearchInput
            )(search_jobs_bound)
            
            self.refine_search_tool = tool(
                args_schema=SearchInput
            )(refine_search_bound)
            
            logger.debug("Tools initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing tools: {e}")
            raise

    def add_to_conversation(self, message: str, sender: str = 'user'):
        """Add a message to conversation history"""
        self.conversation_history.append({
            'text': message,
            'sender': sender,
            'timestamp': datetime.now().isoformat()
        })

    def _search_jobs_impl(self, query: str) -> dict:
        """Search for jobs based on the provided query and conversation context.
        
        Args:
            query: The search query string containing job search criteria
            
        Returns:
            dict: A dictionary containing search results with job matches and status
        """
        logger.debug(f"search_jobs called with query: {query}")
        
        # Add current query to conversation
        logger.debug(f"Adding query to conversation: {query}")
        self.add_to_conversation(query)
        
        # Extract job parameters from conversation history
        logger.debug(f"Current conversation history: {self.conversation_history}")
        params = self.job_search_api.extract_job_params(self.conversation_history)
        logger.debug(f"Extracted job parameters: {params}")
        
        # Run async job search in sync context
        try:
            loop = asyncio.get_event_loop()
            logger.debug("Starting job search")
            job_results = loop.run_until_complete(
                self.job_search_api.search_all(query, params=params)
            )
            logger.debug(f"Job search results status: {job_results.get('status')}")
            logger.debug(f"Number of jobs found: {len(job_results.get('jobs', []))}")
        except Exception as e:
            logger.error(f"Error in job search: {str(e)}")
            return {
                "status": "error",
                "message": f"Error during job search: {str(e)}",
                "search_params": params
            }
        
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

    def _refine_search_impl(self, query: str) -> dict:
        """Refine the job search based on user feedback and additional criteria.
        
        Args:
            query: The refined search query string with additional criteria
            
        Returns:
            dict: A dictionary containing refined search results with job matches and status
        """
        logger.debug(f"Refining search with query: {query}")
        self.add_to_conversation(query)
        return self._search_jobs_impl(query)

    # Create tool properties that return the bound methods
    @property
    def search_jobs(self):
        return self.search_jobs_tool

    @property
    def refine_search(self):
        return self.refine_search_tool

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

    async def get_llm_response(self, message: str) -> str:
        """Get response from Ollama LLM"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama2",
                        "prompt": message,
                        "system": "You are a helpful AI assistant focused on helping users find jobs. Keep responses concise and professional."
                    }
                ) as response:
                    if response.status == 200:
                        full_response = ""
                        async for line in response.content:
                            line_json = json.loads(line)
                            if "response" in line_json:
                                full_response += line_json["response"]
                        return full_response
                    else:
                        return "I apologize, but I'm having trouble processing your request at the moment."
        except Exception as e:
            logger.error(f"Error calling Ollama LLM: {e}")
            return "I apologize, but I'm having trouble connecting to the language model at the moment."

def build_agent():
    matcher = JobMatcher()
    tools = [matcher.search_jobs, matcher.refine_search]
    return initialize_agent(
        tools, 
        matcher.llm, 
        agent="conversational-react-description", 
        verbose=True
    )

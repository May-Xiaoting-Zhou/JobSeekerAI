from fastapi import FastAPI, UploadFile, WebSocket, HTTPException
from pydantic import BaseModel
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import json
import datetime
from scripts.job_search import JobSearchAPI
from ai_agent.job_matcher import build_agent, JobMatcher
from typing import Optional
from utils.logger import get_logger

# Set up logger for this module
logger = get_logger('main')

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {e}")

app = FastAPI()
job_search = JobSearchAPI()
job_matcher = JobMatcher(use_ollama=True)  # Explicitly use Ollama

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@app.websocket("/api/chat")
async def chat_endpoint(websocket: WebSocket):
    logger.info("WebSocket connected")
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            message = ChatMessage(**data)
            # Logic for chat
            # response = {"response": f"Received: {message.message}", "jobs": []}
            response = {"response": "Received: Xiaoting ZHou", "jobs": []}
            await websocket.send_json(response)
        except Exception as e:
            logger.error(f"Error: {e}")
            break

@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile):
    import PyPDF2
    from io import BytesIO
    from nltk.chunk import ne_chunk
    
    # Parse PDF
    pdf_content = await file.read()
    reader = PyPDF2.PdfReader(BytesIO(pdf_content))
    text = "\n".join([page.extract_text() for page in reader.pages])
    
    # Extract entities using NLTK
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    entities = ne_chunk(tagged)
    
    # Extract skills (simplified approach)
    skill_keywords = [
        "python", "javascript", "java", "c++", "react", "angular", "vue", 
        "node", "express", "django", "flask", "fastapi", "sql", "nosql", 
        "mongodb", "postgresql", "mysql", "docker", "kubernetes", "aws", 
        "azure", "gcp", "git", "agile", "scrum", "machine learning", "ai"
    ]
    
    skills = []
    for word in tokens:
        if word.lower() in skill_keywords:
            skills.append(word)
    
    return {"text": text[:500], "skills": skills}

@app.get("/api/jobs/search")
async def search_jobs(query: str, location: str = "Remote"):
    results = await job_search.search_all(query, location)
    return results

@app.post("/chat")
async def chat_message(message: ChatMessage):
    try:
        logger.debug("====== New Chat Message ======")
        logger.debug(f"Received message: {message.message}")
        logger.debug(f"Conversation ID: {message.conversation_id}")
        
        # First, get LLM response using JobMatcher's Ollama implementation
        logger.debug("Getting LLM response...")
        llm_response = await job_matcher.get_llm_response(message.message)
        logger.debug(f"LLM response received: {llm_response[:100]}...")
        
        # Add message to conversation history
        logger.debug("Adding message to conversation history")
        job_matcher.add_to_conversation(message.message)
        
        # Check for job search intent
        job_related_words = ['job', 'work', 'position', 'hiring', 'career', 'employment']
        has_job_intent = any(word in message.message.lower() for word in job_related_words)
        logger.debug(f"Has job search intent: {has_job_intent}")
        
        if has_job_intent:
            try:
                logger.debug("Starting job search...")
                # Use job matcher to find relevant positions
                results = job_matcher.search_jobs.invoke({"query": message.message})
                logger.debug(f"Job search completed. Status: {results.get('status')}")
                logger.debug(f"Full results: {json.dumps(results, indent=2)}")
                
                if results["status"] == "success":
                    # Combine LLM response with job search results
                    logger.debug("Combining LLM response with job results")
                    combined_response = f"{llm_response}\n\nI found some relevant job opportunities:\n\n{results['message']}"
                    return {"response": combined_response}
                else:
                    logger.debug("No successful job results, returning prompt for more details")
                    return {
                        "response": f"{llm_response}\n\nI couldn't find specific job listings matching your criteria. Could you provide more details about what type of position you're looking for?"
                    }
            except Exception as search_error:
                logger.error(f"Error during job search: {str(search_error)}")
                return {
                    "response": f"{llm_response}\n\nI encountered an error while searching for jobs. Please try again with more specific criteria."
                }
        
        # For non-job queries, just return the LLM response
        logger.debug("No job intent detected, returning LLM response only")
        return {"response": llm_response}
        
    except Exception as e:
        logger.error(f"Error in chat_message: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

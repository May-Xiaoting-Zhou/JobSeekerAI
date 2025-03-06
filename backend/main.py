from fastapi import FastAPI, UploadFile, WebSocket, HTTPException
from pydantic import BaseModel
import spacy
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import json
import datetime
from scripts.job_search import JobSearchAPI
from ai_agent.job_matcher import build_agent, JobMatcher
from typing import Optional

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

nlp = spacy.load("en_core_web_sm")  # Load Spacy model

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

@app.websocket("/api/chat")
async def chat_endpoint(websocket: WebSocket):
    print("WebSocket connected")
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            message = ChatMessage(**data)
            # Logic for chat
            # response = {"response": f"Received: {message.message}", "jobs": []}
            response = {"response": f"Received: {"Xiaoting ZHou"}", "jobs": []}
            await websocket.send_json(response)
        except Exception as e:
            print(f"Error: {e}")
            break

@app.post("/api/resume/parse")
async def parse_resume(file: UploadFile):
    import PyPDF2
    from io import BytesIO
    
    # Parse PDF
    pdf_content = await file.read()
    reader = PyPDF2.PdfReader(BytesIO(pdf_content))
    text = "\n".join([page.extract_text() for page in reader.pages])
    
    # Extract entities
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    
    return {"text": text[:500], "skills": skills}

@app.get("/api/jobs/search")
async def search_jobs(query: str, location: str = "Remote"):
    results = await job_search.search_all(query, location)
    return results

@app.post("/chat")
async def chat_message(message: ChatMessage):
    try:
        print(f"\n[DEBUG] ====== New Chat Message ======")
        print(f"[DEBUG] Received message: {message.message}")
        print(f"[DEBUG] Conversation ID: {message.conversation_id}")
        
        # First, get LLM response using JobMatcher's Ollama implementation
        print("[DEBUG] Getting LLM response...")
        llm_response = await job_matcher.get_llm_response(message.message)
        print(f"[DEBUG] LLM response received: {llm_response[:100]}...")
        
        # Add message to conversation history
        print("[DEBUG] Adding message to conversation history")
        job_matcher.add_to_conversation(message.message)
        
        # Check for job search intent
        job_related_words = ['job', 'work', 'position', 'hiring', 'career', 'employment']
        has_job_intent = any(word in message.message.lower() for word in job_related_words)
        print(f"[DEBUG] Has job search intent: {has_job_intent}")
        
        if has_job_intent:
            try:
                print("[DEBUG] Starting job search...")
                # Use job matcher to find relevant positions
                results = job_matcher.search_jobs.invoke({"query": message.message})
                print(f"[DEBUG] Job search completed. Status: {results.get('status')}")
                print(f"[DEBUG] Full results: {json.dumps(results, indent=2)}")
                
                if results["status"] == "success":
                    # Combine LLM response with job search results
                    print("[DEBUG] Combining LLM response with job results")
                    combined_response = f"{llm_response}\n\nI found some relevant job opportunities:\n\n{results['message']}"
                    return {"response": combined_response}
                else:
                    print("[DEBUG] No successful job results, returning prompt for more details")
                    return {
                        "response": f"{llm_response}\n\nI couldn't find specific job listings matching your criteria. Could you provide more details about what type of position you're looking for?"
                    }
            except Exception as search_error:
                print(f"[ERROR] Error during job search: {str(search_error)}")
                return {
                    "response": f"{llm_response}\n\nI encountered an error while searching for jobs. Please try again with more specific criteria."
                }
        
        # For non-job queries, just return the LLM response
        print("[DEBUG] No job intent detected, returning LLM response only")
        return {"response": llm_response}
        
    except Exception as e:
        print(f"[ERROR] Error in chat_message: {str(e)}")
        print(f"[ERROR] Error type: {type(e)}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
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
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
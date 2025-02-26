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
job_matcher = JobMatcher()

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

async def get_llm_response(user_message: str) -> str:
    """Get response from Ollama LLM"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": user_message,
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
        print(f"Error calling LLM: {e}")
        return "I apologize, but I'm having trouble connecting to my language model at the moment."

@app.get("/api/jobs/search")
async def search_jobs(query: str, location: str = "Remote"):
    results = await job_search.search_all(query, location)
    return results

@app.post("/chat")
async def chat_message(message: ChatMessage):
    try:
        print(f"Received message: {message.message}")  # Debug log
        
        # First, get LLM response
        llm_response = await get_llm_response(message.message)
        print(f"LLM response: {llm_response}")  # Debug log
        
        # Add message to conversation history
        job_matcher.add_to_conversation(message.message)
        
        # Check for job search intent
        if any(word in message.message.lower() for word in ['job', 'work', 'position', 'hiring', 'career', 'employment']):
            # Use job matcher to find relevant positions
            results = job_matcher.search_jobs(message.message)
            print(f"Job search results: {json.dumps(results, indent=2)}")  # Debug log
            
            if results["status"] == "success":
                # Combine LLM response with job search results
                combined_response = f"{llm_response}\n\nI found some relevant job opportunities:\n\n{results['message']}"
                return {"response": combined_response}
            else:
                # Return LLM response with a prompt for more details
                return {
                    "response": f"{llm_response}\n\nI couldn't find specific job listings matching your criteria. Could you provide more details about what type of position you're looking for?"
                }
        
        # For non-job queries, just return the LLM response
        return {"response": llm_response}
        
    except Exception as e:
        print(f"Error in chat_message: {e}")  # Debug log
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
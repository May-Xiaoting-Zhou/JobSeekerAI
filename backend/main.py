from fastapi import FastAPI, UploadFile, WebSocket
from pydantic import BaseModel
import spacy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")  # 加载Spacy模型

class ChatMessage(BaseModel):
    message: str

@app.websocket("/api/chat")
async def chat_endpoint(websocket: WebSocket):
    print("WebSocket connected")
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            message = ChatMessage(**data)
            # 处理对话逻辑
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
    
    # 解析PDF
    pdf_content = await file.read()
    reader = PyPDF2.PdfReader(BytesIO(pdf_content))
    text = "\n".join([page.extract_text() for page in reader.pages])
    
    # 提取实体
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    
    return {"text": text[:500], "skills": skills}

@app.post("/chat")
async def chat_message(message: ChatMessage):
    print(f"==========Backend received message: {message.message}")  # Debug print
    # Here you can add your AI logic
    response = f"I am Xiaoting Zhou, your AI assistant. You said: {message.message}"
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
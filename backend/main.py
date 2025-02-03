from fastapi import FastAPI, UploadFile, WebSocket
from pydantic import BaseModel
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")  # 加载Spacy模型

class ChatMessage(BaseModel):
    user_id: str
    content: str

@app.websocket("/api/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # 处理对话逻辑
        response = {"response": "已找到3个匹配职位", "jobs": [...]}
        await websocket.send_json(response)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
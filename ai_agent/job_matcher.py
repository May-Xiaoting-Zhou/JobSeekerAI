from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class JobMatcher:
    def __init__(self):
        self.job_db = []  # 示例职位数据
        self.encoder = model
    
    @tool
    def search_jobs(self, query: str) -> list:
        """根据自然语言查询搜索职位"""
        query_vec = self.encoder.encode(query)
        scores = []
        for job in self.job_db:
            job_vec = self.encoder.encode(job["description"])
            scores.append(np.dot(query_vec, job_vec))
        return sorted(zip(self.job_db, scores), key=lambda x: -x[1])[:3]

def build_agent():
    llm = ChatOpenAI(temperature=0)
    tools = [JobMatcher().search_jobs]
    return initialize_agent(
        tools, llm, agent="conversational-react-description", verbose=True
    )
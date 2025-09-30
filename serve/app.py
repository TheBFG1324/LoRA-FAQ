from fastapi import FastAPI
from pydantic import BaseModel
from .loader import answer

app = FastAPI()

class Q(BaseModel):
    question: str

@app.post("/answer")
def post_answer(q: Q):
    return {"answer": answer(q.question)}

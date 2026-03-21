from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama
import os, time

app = FastAPI()


# Carrega modelo
llm = Llama(
    # model_path="models/TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf",
     model_path="models/mistral-7b-instruct-v0.1.Q4_0.gguf",
    n_ctx=1024,
    n_threads=os.cpu_count()
)

class Request(BaseModel):
    prompt: str

@app.post("/chat")
def chat(req: Request):

    start = time.time()

    output = llm(
        prompt = f"""
            <s>[INST]
                You are a helpful AI assistant.
                Always respond clearly and directly.
            
                {req.prompt}
            [/INST]
            """,
        max_tokens=150,
        temperature=0.7
    )
    
    end = time.time()

    return {
        "response": output["choices"][0]["text"],
        "total_time": end - start
    }
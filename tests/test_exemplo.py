import pytest
from app.main import chat

def test_testando_post_chat():
    resposta =  {
        "response": "resposta do llm",
        "total_time": 5.78,
        "model": "caminho/do/modelo"
    }
    assert resposta

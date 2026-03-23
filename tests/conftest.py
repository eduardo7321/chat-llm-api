# tests/conftest.py
import pytest
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importe sua aplicação
try:
    from app.main import app
except ImportError:
    try:
        from main import app
    except ImportError:
        # Se não conseguir importar, falhe com mensagem clara
        raise ImportError("Não foi possível importar o app. Verifique a estrutura do projeto.")

@pytest.fixture(scope="session")
def client():
    """Fixture para o cliente de teste FastAPI"""
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture
def sample_prompt():
    """Fixture com um prompt de exemplo"""
    return {
        "prompt": "Qual é a capital do Brasil?"
    }
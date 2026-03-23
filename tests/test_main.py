# tests/test_main.py
import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import sys
import os

# Adiciona o diretório pai ao path para importar o app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa o app do arquivo correto
from app.main import app

client = TestClient(app)

# Fixture para mock do LLM
@pytest.fixture
def mock_llm():
    """Mock do LLM para evitar chamadas reais"""
    # Patch no caminho correto: app.main.llm
    with patch('app.main.llm') as mock:
        # Configura o mock para retornar uma estrutura simulada
        mock.return_value = {
            "choices": [
                {
                    "text": "Esta é uma resposta simulada do assistente de IA."
                }
            ]
        }
        # Também mocka o model_path
        mock.model_path = "models/mock-model.gguf"
        yield mock

# Teste básico - sucesso (com mock)
def test_chat_endpoint_success(mock_llm):
    """Testa o endpoint /chat com uma requisição válida usando mock"""
    
    request_data = {
        "prompt": "Qual é a capital do Brasil?"
    }
    
    response = client.post("/chat", json=request_data)
    
    # Verificações
    assert response.status_code == 200
    data = response.json()
    
    # Verifica estrutura da resposta
    assert "response" in data
    assert "total_time" in data
    assert "model" in data
    
    # Verifica conteúdo da resposta
    assert isinstance(data["response"], str)
    assert isinstance(data["total_time"], float)
    assert data["total_time"] >= 0
    assert data["response"] == "Esta é uma resposta simulada do assistente de IA."
    
    # Verifica que o mock foi chamado corretamente
    mock_llm.assert_called_once()
    
    # Verifica os argumentos da chamada
    call_args = mock_llm.call_args[1]
    assert "prompt" in call_args
    assert "max_tokens" in call_args
    assert "temperature" in call_args
    assert call_args["max_tokens"] == 150
    assert call_args["temperature"] == 0.7

# Teste com prompt vazio
def test_chat_endpoint_empty_prompt():
    """Testa o comportamento com prompt vazio"""
    
    request_data = {
        "prompt": ""
    }
    
    response = client.post("/chat", json=request_data)
    
    # Com Pydantic, prompt vazio é aceito como string válida
    # Deve retornar 200 mesmo com prompt vazio
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)

# Teste com payload inválido
def test_chat_endpoint_invalid_payload():
    """Testa com payload inválido (sem campo prompt)"""
    
    request_data = {
        "wrong_field": "teste"
    }
    
    response = client.post("/chat", json=request_data)
    
    # Deve retornar erro 422 (Unprocessable Entity) por causa do Pydantic
    assert response.status_code == 422

# Teste com formato de dados incorreto
def test_chat_endpoint_wrong_data_type():
    """Testa com tipo de dado incorreto"""
    
    request_data = {
        "prompt": 12345  # prompt como número, não string
    }
    
    response = client.post("/chat", json=request_data)
    
    # Deve retornar erro de validação 422
    assert response.status_code == 422

# Teste de performance - marcado como lento
@pytest.mark.slow
def test_chat_endpoint_performance():
    """Teste de performance - executa chamada real ao LLM"""
    
    request_data = {
        "prompt": "Teste de performance"
    }
    
    # Mede o tempo de uma requisição
    start = time.time()
    response = client.post("/chat", json=request_data)
    elapsed = time.time() - start
    
    assert response.status_code == 200
    data = response.json()
    
    print(f"\nTempo total da requisição: {elapsed:.2f}s")
    print(f"Tempo de processamento do LLM: {data['total_time']:.2f}s")
    print(f"Modelo usado: {data['model']}")
    print(f"Resposta: {data['response'][:100]}...")
    
    # Ajuste este limite conforme sua necessidade
    # Para Llama 3.1 8B, 30 segundos pode ser razoável
    assert elapsed < 60.0

# Teste simulando erro do LLM
def test_chat_endpoint_llm_error(mock_llm):
    """Testa comportamento quando o LLM falha"""
    
    # Configura o mock para lançar uma exceção
    mock_llm.side_effect = Exception("Erro simulado no LLM")
    
    request_data = {
        "prompt": "Teste de erro"
    }
    
    response = client.post("/chat", json=request_data)
    
    # Deve retornar erro 500 (Internal Server Error)
    assert response.status_code == 500

# Teste com diferentes prompts
@pytest.mark.parametrize("prompt", [
    "Qual é a capital do Brasil?",
    "Explique o que é Python",
    "Faça uma piada",
    "O que é inteligência artificial?"
])
def test_chat_endpoint_different_prompts(prompt, mock_llm):
    """Testa o endpoint com diferentes prompts"""
    
    request_data = {"prompt": prompt}
    response = client.post("/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Esta é uma resposta simulada do assistente de IA."

# Teste de integração real (opcional)
@pytest.mark.integration
def test_chat_endpoint_integration():
    """Teste de integração - executa com modelo real"""
    
    request_data = {
        "prompt": "Diga 'Olá, teste funcionando!'"
    }
    
    response = client.post("/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "total_time" in data
    assert "model" in data
    assert len(data["response"]) > 0
    print(f"\nResposta real: {data['response']}")
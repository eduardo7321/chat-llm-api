# LLM API com FastAPI + Docker

Este projeto é uma API simples utilizando **FastAPI** para rodar um modelo de linguagem (LLM) localmente usando `llama-cpp-python` sem a necessidade de GPU.

---

## Tecnologias utilizadas

- Python 3.10
- FastAPI
- Uvicorn
- llama-cpp-python
- Docker

---
## Adicionando modelos de LLM

Na raiz do projeto crie uma pasta chamada models e adicione dentro delas seus modelos
- Você pode baixar modelos de llms no HuggingFace
- Dê preferências a modelos pequenos, que foram bem testados e são confiáveis, do tipo gguf

## Estrutura do projeto

| Pasta/Arquivo | Descrição |
|--------------|-----------|
| `app/` | Código fonte principal do backend da aplicação |
| `models/` | Diretório contendo os modelos LLM quantizados (GGUF) |
| `tests/` | Testes unitários e de integração utilizando pytest |
| `Dockerfile` | Arquivo para containerização da aplicação |
| `Makefile` | Automação de tarefas como execução de testes |
| `pytest.ini` | Configurações do framework de testes pytest |
| `requirements.txt` | Lista de dependências Python do projeto |
| `.env.example` | Template para configuração de variáveis de ambiente |

> **Nota:** Os modelos LLM são arquivos de grande porte. Certifique-se de que eles estão no formato GGUF (quantizados) para otimizar o uso de memória e performance.

---

## Como funciona

A API recebe um prompt via POST e retorna:

- resposta do modelo
- tempo total de execução

---

## Build da imagem Docker

Dentro da pasta do projeto, execute:

```bash
docker build -t llm-api .
```

## Executar o container

```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  llm-api
```


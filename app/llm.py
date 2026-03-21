from llama_cpp import Llama
import os
import time

# Caminho para o seu modelo
# model_path = "./models/mistral-7b-instruct-v0.1.Q4_0.gguf"
model_path = "./models/TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf"


inicio = time.time()

# Carrega o modelo
llm = Llama(
    model_path=model_path,
    n_ctx=1024,      # contexto
    n_threads=os.cpu_count()    # ajuste conforme seu CPU
)

print(f'Quantidade de CPU: {llm.n_threads}')

# Prompt simples (formato instruct do Mistral)
prompt = """<s>[INST] O que é machine learning? [/INST]"""

# Geração
output = llm(
    prompt,
    max_tokens=100,
    temperature=0.5,
    stop=["</s>"]
)

# Print resposta
print(output["choices"][0]["text"])

fim = time.time()
print('-----------')
print(f'Tempo total: {fim - inicio:.2f}')
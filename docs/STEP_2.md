# 🧠 Manual de Estudo: IA Local com llama.cpp & LangChain

Este guia foca nos pilares técnicos para rodar e orquestrar LLMs localmente, adaptado para os seus perfis de hardware (i5 12ª Gen e GTX 1650).

---

## 🛠️ 1. O Motor: llama.cpp
O `llama.cpp` permite rodar modelos em C++ com altíssima performance. Para dominá-lo, você precisa entender estes parâmetros:

### Parâmetros de Performance
* **n_threads (-t):** No seu **i5 (Trabalho)**, use **6**. No **Linux (Pessoal)**, use **4** (deixando a GPU trabalhar).
* **n_gpu_layers (-ngl):** * *Trabalho:* **0** (Uso exclusivo de CPU).
    * *Pessoal:* **20 a 35** (Descarrega camadas para os 4GB da GTX 1650).
* **n_batch (-b):** Tamanho do lote para processamento. **512** é o padrão equilibrado.
* **n_ctx (-c):** O tamanho da "memória" da sessão. Comece com **2048**. Aumentar para 8192 dobra o uso de RAM/VRAM.

---

## 🌟 2. Modelo em Destaque: Hermes-2-Pro-Llama-3-8B
Este modelo é uma versão "turbinada" do Llama-3 da Meta, treinado pela **Nous Research**.

### Por que ele é especial para você (Dev Web)?
* **Function Calling (Pro):** É excelente para entender quando precisa "chamar uma função". No LangChain, isso é vital para integrar a IA com seu banco de dados MySQL ou APIs do Laravel.
* **Structured Output:** Ele é treinado para responder em **JSON** de forma muito estável. Perfeito para sistemas onde a IA precisa devolver dados que seu PHP vai processar.
* **Quantização Q4_K_M:** Ocupa cerca de **4.92 GB**. 
    * No **Trabalho**: Roda rápido na CPU.
    * No **Pessoal**: Cabe quase inteiramente nos 4GB da GTX 1650 (ajuste as camadas para não estourar a VRAM).

---

## 🦜 3. O Orquestrador: LangChain
O LangChain conecta o modelo ao seu código (PHP/Python) e a dados externos.

### Arquitetura RAG (Aplicações Reais)
Para fazer a IA ler seus arquivos `.php` da prefeitura:
1.  **Loaders:** Leem seus arquivos.
2.  **Text Splitters:** Quebram o código em pedaços lógicos.
3.  **Embeddings:** Transformam o código em vetores matemáticos.
4.  **Vector Store:** Banco de dados (Chroma ou FAISS) que guarda esses vetores.

---

## 🚀 Implementação de Referência (Python)

```python
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.messages import HumanMessage, SystemMessage

# Instância configurada para o Hermes-2-Pro
llm = ChatLlamaCpp(
    model_path="models/Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf",
    n_gpu_layers=28,    # Ajuste fino para GTX 1650
    n_ctx=4096,
    n_threads=6,
    temperature=0.1,    # Estabilidade para código e JSON
)

messages = [
    SystemMessage(content="Você é um especialista em JSON e APIs Laravel."),
    HumanMessage(content="Gere um JSON com 3 usuários fakes para um seeder PHP.")
]

print(llm.invoke(messages).content)
```

---

## 🔬 Roadmap de Testes por Ambiente

### No Notebook do Trabalho (Foco: Estabilidade)
* **Stress Test:** Monitore como o Hermes se comporta com contextos longos (acima de 4k tokens).

### No Notebook Pessoal (Foco: Performance)
* **NVIDIA Toolkit:** No Linux, certifique-se de que o `llama-cpp-python` foi instalado com suporte a **CUDA** para aproveitar a GTX 1650.

---

## 📔 Termos Desconhecidos para Pesquisa
* **Function Calling:** Capacidade do modelo de estruturar argumentos para funções externas.
* **JSON Mode:** Configuração que força a IA a responder apenas em formato JSON válido.
* **CUDA Toolkit:** Drivers e bibliotecas necessários para a GPU NVIDIA rodar a IA.
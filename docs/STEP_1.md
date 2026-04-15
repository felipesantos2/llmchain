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

### Conceitos de Arquivo
* **GGUF:** O formato essencial. Ele agrupa pesos e metadados em um único arquivo.
* **Quantização (K-Quants):**
    * **Q4_K_M:** O "padrão ouro". Perda mínima de inteligência com grande redução de peso.
    * **Q2_K / Q3_K:** Use apenas se quiser testar modelos gigantes (como 30B) no seu PC pessoal.

---

## 🦜 2. O Orquestrador: LangChain
O LangChain conecta o modelo ao seu código (PHP/Python) e a dados externos.

### Componentes Chave
* **ChatLlamaCpp:** Classe específica para modelos de chat. Gerencia o "Prompt Template" automaticamente para você.
* **PromptTemplates:** Onde você define a "personalidade" da IA.
* **Chains (Cadeias):** Sequências de tarefas. Ex: Buscar no banco -> Resumir -> Traduzir.
* **Memory:** Como o LangChain mantém o histórico da conversa entre um request HTTP e outro (essencial para o seu Laravel).

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

# Instância configurada para o PC PESSOAL (Linux + GPU)
llm = ChatLlamaCpp(
    model_path="models/llama-3-8b-instruct.Q4_K_M.gguf",
    n_gpu_layers=30,    # Offloading para GTX 1650
    n_ctx=4096,         # Janela de contexto
    n_threads=4,        # Threads de CPU
    temperature=0.1,    # Baixa temperatura para respostas técnicas
    f16_kv=True,        # Cache de alta precisão
)

messages = [
    SystemMessage(content="Você é um arquiteto de software especializado em TALL Stack."),
    HumanMessage(content="Como estruturar um Service Pattern no Laravel?")
]

print(llm.invoke(messages).content)
```

---

## 🔬 Roadmap de Testes por Ambiente

### No Notebook do Trabalho (Foco: Estabilidade)
* **Teste de Stress:** Rode o modelo com `-t 4`, `-t 6` e `-t 8` e monitore a temperatura do i5.
* **LangChain + PDF:** Crie um script que lê um manual de sistemas da prefeitura e responde dúvidas.

### No Notebook Pessoal (Foco: Performance)
* **Ollama no Linux:** Instale o Ollama (`curl -fsSL https://ollama.com/install.sh | sh`) e veja como ele automatiza o gerenciamento do llama.cpp.
* **Vision/OCR:** Use o modelo **LLaVA** para analisar prints de erros de tela do seu sistema Java Desktop.

---

## 📔 Termos Desconhecidos para Pesquisa
* **KV Cache:** Como a IA reutiliza cálculos anteriores para responder mais rápido.
* **Context Window Overflow:** O que acontece quando a conversa fica longa demais.
* **Prompt Injection:** Riscos de segurança ao usar dados de usuários nos prompts.
* **CUDA Toolkit:** Necessário no Linux para sua GTX 1650 "falar" com a IA.
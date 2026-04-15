from dotenv import load_dotenv  # ty:ignore[unresolved-import]

from rich.console import Console  # ty:ignore[unresolved-import]

from datetime import datetime
from pathlib import Path

from langchain_community.chat_models import ChatLlamaCpp  # ty:ignore[unresolved-import]

import multiprocessing


load_dotenv()


current_date = datetime.now().strftime("%Y-%m-%d")
current_dir = Path(__file__).resolve().parent

"""
    Model in HuggingFace: 
        Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf
        tiny-audio.Q4_K_M.gguf]
        
    Format: GGUF
        link: https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF
              https://huggingface.co/mazesmazes/tiny-audio
"""

model_name = "Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf"

local_model = str(current_dir / "llm-models" / model_name)

console = Console()


# class WeatherInput(BaseModel):
#     location: str = Field(description="The city and state, e.g. San Francisco, CA")
#     unit: str = Field(enum=["celsius", "fahrenheit"])


# @tool("get_current_weather", args_schema=WeatherInput)
# def get_weather(location: str, unit: str):
#     """Get the current weather in a given location"""
#     return f"Now the weather in {location} is 22 {unit}"


# llm_with_tools = llm.bind_tools(
#     tools=[get_weather],
#     tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
# )

# ai_msg = llm_with_tools.invoke(
#     "what is the weather like in HCMC in celsius",
# )

# ai_msg.tool_calls


try:
    llm = ChatLlamaCpp(
        temperature=0.7,
        model_path=local_model,
        n_ctx=3000,
        n_gpu_layers=0,
        n_batch=500,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        max_tokens=512,
        n_threads=multiprocessing.cpu_count() - 1,
        repeat_penalty=1.5,
        top_p=0.5,
        verbose=True,
    )

    messages = [
        (
            "system",
            "Você é um especilista em jogos e sua paixão se encontra no mundo Indie da força",
        ),
        ("human", """
            Dê exemplos de uso do modulo multiprocessing do Python.
            Defina sua diferença com base nas outras opções que temos no Python, Threads, Async e Concurrence. 
            Liste todas as opções que temos para trabalahar com multitarefas no Python. Acabei de me lembrar do Event-loop 'Async'.
        """),
    ]

    ai_msg = llm.invoke(input=messages)
    console.log(ai_msg.content)
except Exception as e:
    console.log(f"Erro: {e}")

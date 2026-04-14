from dotenv import load_dotenv

from rich.console import Console

from datetime import datetime
from pathlib import Path

from langchain_community.chat_models import ChatLlamaCpp
from langchain.tools import tool
from pydantic import BaseModel, Field

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

model_name = "tiny-audio.Q4_K_M.gguf"

local_model = str(current_dir / "llm-models" / model_name)

console = Console()

llm = ChatLlamaCpp(
    temperature=0.5,
    model_path=local_model,
    n_ctx=10000,
    n_gpu_layers=8,
    n_batch=300,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    max_tokens=300,
    n_threads=multiprocessing.cpu_count() - 1,
    repeat_penalty=1.5,
    top_p=0.5,
    verbose=True,
)

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

messages = [
    (
        "system",
        "You are a helpful assistant that translates Portuguese to English. Translate the user sentence.",
    ),
    ("human", "Bom dia, Cara!"),
]

ai_msg = llm.invoke(input=messages)


console.log(ai_msg.content)

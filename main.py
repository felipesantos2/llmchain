from src.main import output

from rich.console import Console
from pathlib import Path

console = Console()

model_name = "Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf"
current_dir = Path(__file__).resolve().parent
model_path = str(current_dir / "llms" / model_name)

"""
    Model in HuggingFace: 
        Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf
        tiny-audio.Q4_K_M.gguf
        
    Format: GGUF
        link: https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF
              https://huggingface.co/mazesmazes/tiny-audio
"""

if __name__ == "__main__":
    try:
        output(model_path)
    except Exception as e:
        console.log(f" Exception: {e}")

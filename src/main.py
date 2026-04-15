from dotenv import load_dotenv

from rich.console import Console

from langchain_community.chat_models import ChatLlamaCpp

import multiprocessing

console = Console()

load_dotenv()


def output(model_path: str) -> None:
    llm = ChatLlamaCpp(
        temperature=0.9,
        model_path=model_path,
        n_ctx=9000,
        n_gpu_layers=45,
        n_batch=300,
        max_tokens=300,
        n_threads=multiprocessing.cpu_count() - 1,
        repeat_penalty=1.5,
        top_p=0.5,
        verbose=True,
    )
    messages = [
        (
            "system",
            "Você é um especialistam em Games. Mas do lado indie da força.",
        ),
        (
            "human",
            "Me indique um com jogo Indie e por favor não vamos de 'Celeste'. Quero algo totalmente novo.",
        ),
    ]

    ai_msg = llm.invoke(input=messages)

    console.log(ai_msg.content)


if __name__ == "__main__":
    exit()

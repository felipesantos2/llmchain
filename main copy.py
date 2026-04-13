from dotenv import dotenv_values
from rich.console import Console

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

import os
import getpass

from datetime import datetime

from tools import get_my_favorite_indie_game, get_random_indie_game


CONFIG = dotenv_values(".env")
current_date = datetime.now().strftime("%Y-%m-%d")
console = Console()

api_key = CONFIG.get("GOOGLE_API_KEY", None)
ai_model = CONFIG.get("MODEL", None)

if ai_model is None:
    ai_model = ""

if api_key is None:
    api_key = ""

SYSTEM_PROMPT = """
  Você é um jornalista especialista no mundo dos Games, com uma forte paixão pelo Lado INDIE da força.
    Você tem certo receio quanto as práticas da nintendo e morre de medo do monopólio estabelecido pela Sony nos últimos Anos
        Você tem acesso a duas ferramentas:
        - get_my_favorite_indie_game: use esta ferramenta para obter a o jogo favorito do usuário, caso ele já esteja salvo em banco
        - get_random_indie_game: use esta ferramenta  para indicar um novo jogo para o usuário
        Se um usuário lhe perguntar sobre jogos, certifique-se de saber a sua preferência. 
    """
# agent = create_agent(
#     model="gemini-3.1-pro-preview",
#     tools=[get_my_favorite_indie_game],
#     system_prompt=SYSTEM_PROMPT,
# )

model = ChatGoogleGenerativeAI(
    model=ai_model,
    api_key=api_key,
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=1,
)


def main():
    # agent.invoke({"messages": [{"role": "user", "content": "me indique im jogo"}]})

    ai_msg = model.invoke("Olá, Com o que você pode me ajudar?")

    console.log(ai_msg)


if __name__ == "__main__":
    main()

from dotenv import dotenv_values
from rich.console import Console

from langchain_google_genai import ChatGoogleGenerativeAI

from datetime import datetime

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

history = []


def main():
    try:
        model = ChatGoogleGenerativeAI(
            model=ai_model,
            api_key=api_key,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
            max_retries=1,
        )

        while True:
            console.log("Digite 'sair' para fechar: ")
            msg = input("Digite: ")

            if msg in ["sair", "SAIR", "Sair", "Exit", "exit"]:
                console.log("Historico: ", history)
                exit()

            ai_response = model.invoke(input=msg)

            history.append(
                {
                    "human": msg,
                    "ai": ai_response,
                }
            )

            console.log(ai_response.content)
    except Exception as e:
        console.log(f"Error: {e}")


if __name__ == "__main__":
    main()

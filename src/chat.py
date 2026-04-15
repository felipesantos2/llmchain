from dotenv import dotenv_values # ty:ignore[unresolved-import]
from rich.console import Console # ty:ignore[unresolved-import]

from langchain_google_genai import ChatGoogleGenerativeAI  # ty:ignore[unresolved-import]

from datetime import datetime

CONFIG = dotenv_values(".env")
current_date = datetime.now().strftime("%Y-%m-%d")

console = Console()

API_KEY = CONFIG.get("GOOGLE_API_KEY", None)
LLM_MODEL = CONFIG.get("MODEL", None)

if LLM_MODEL is None:
    LLM_MODEL = ""

if API_KEY is None:
    API_KEY = ""


history: list[dict] = []


def main():
    try:
        model = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            api_key=API_KEY,
            temperature=1.0,
            max_tokens=None,
            timeout=None,
            max_retries=1,
        )

        while True:
            console.log("'Digite sair para fechar:'  ")
            msg = input("Digite: ")

            if msg in ["sair", "SAIR", "Sair", "Exit", "exit", "EXIT", "clear", "Clear", "CLEAR"]:
                console.log("Historico: ", history)
                exit()

            ai_response = model.invoke(input=msg)

            history.append(
                {
                    "human_message": msg,
                    "ai_response": ai_response,
                }
            )

            console.log(ai_response.content)
    except Exception as e:
        console.log(f"Error: {e}")


if __name__ == "__main__":
    main()

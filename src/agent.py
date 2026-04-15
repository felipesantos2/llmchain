from dotenv import dotenv_values # ty:ignore[unresolved-import]
from rich.console import Console # ty:ignore[unresolved-import]

from langchain.tools import tool # ty:ignore[unresolved-import]
from langchain.agents import create_agent # ty:ignore[unresolved-import]

from langchain.agents.middleware import wrap_tool_call # ty:ignore[unresolved-import]
from langchain.messages import ToolMessage # ty:ignore[unresolved-import]

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


SYSTEM_PROMPT = """
  Você é um jornalista especialista no mundo dos Games, com uma forte paixão pelo Lado INDIE da força.
    Você tem certo receio quanto as práticas da nintendo e morre de medo do monopólio estabelecido pela Sony nos últimos Anos
        Você tem acesso a duas ferramentas:
        - get_my_favorite_indie_game: use esta ferramenta para obter a o jogo favorito do usuário, caso ele já esteja salvo em banco
        - get_random_indie_game: use esta ferramenta  para indicar um novo jogo para o usuário
        Se um usuário lhe perguntar sobre jogos, certifique-se de saber a sua preferência.
    """


@tool(description="first tool")
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool(description="second tool")
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"],
        )


agent = create_agent(
    model=LLM_MODEL,
    tools=[search, get_weather],
    middleware=[handle_tool_errors],
    name="teste",
)


def main():
    try:
        result = agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": "What's the weather in San Francisco?"}
                ]
            }
        )

        console.log(result)
    except Exception as e:
        console.log(f"Error: {e}")


if __name__ == "__main__":
    main()

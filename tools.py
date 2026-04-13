from langchain.tools import tool


@tool(description="Retorna o jogo favorito do Usuário")
def get_my_favorite_indie_game() -> str:
    return "O jogo favorito do usuáŕio é o POU"


@tool(description="Retorna o jogo favorito do Usuário")
def get_random_indie_game() -> str:
    return "O jogo favorito do usuáŕio é o POU"

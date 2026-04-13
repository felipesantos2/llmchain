from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
import getpass
import os

@tool
def get_weather_tool(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

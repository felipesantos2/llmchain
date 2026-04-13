from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
import getpass
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

agent = create_agent(
    model="gemini-3.1-pro-preview",
    tools=[get_weather_tool],
    system_prompt="You are a helpful assistant",
)

def main():
    agent.invoke(
        {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
    )


if __name__ == "__main__":
    main()

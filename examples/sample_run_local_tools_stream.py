"""Antropic Sample"""
import os

from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic, MessageStopEvent, TextEvent
from toolhouse import Toolhouse, Provider # Import the Toolhouse SDK

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

local_tools = [
    {
        "name": "hello",
        "description": "The user receives a customized hello message from a city and returns it to the user.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "The city where you are from"}},
            "required": ["city"],
        },
    }
]

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize Toolhouse with the Anthropic provider
th = Toolhouse(api_key=TH_API_KEY, provider=Provider.ANTHROPIC)
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def hello_tool(city: str):
    """Return a Hello message from a specific city."""
    return f"Hello from {city}!!!"


messages: List = [{"role": "user", "content": "Can I get a hello from Rome?"}]

with client.messages.stream(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages # Retrieve tools installed from Toolhouse
) as stream:
    for block in stream:
        if isinstance(block, MessageStopEvent):
            messages += th.run_tools(block.message) # Run the tools using the Toolhouse client with the created message
        elif isinstance(block, TextEvent):
            print(block.text, end="", flush=True)


with client.messages.stream(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages # Retrieve tools installed from Toolhouse
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

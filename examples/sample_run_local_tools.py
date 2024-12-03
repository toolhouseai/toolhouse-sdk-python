"""Antropic Sample"""
import os

from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import TextBlock
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

response = client.messages.create(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages # Retrieve tools installed from Toolhouse
)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(response)

response = client.messages.create(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages # Retrieve tools installed from Toolhouse
)
if isinstance(response.content[0], TextBlock):
    print(response.content[0].text)

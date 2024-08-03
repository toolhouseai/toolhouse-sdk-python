"""Antropic Sample"""
import os
from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic, MessageStopEvent, TextEvent
from toolhouse import Toolhouse, Provider

load_dotenv()

TOKEN = os.getenv("ANTHROPIC_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_BEARER_TOKEN")

local_tools = [
    {
        'name': 'hello',
        'description': 'The user receive a customized hello message from a city and return it to the user', 
        'input_schema': {
                    'type': 'object',
                    'properties': {
                        'city': {'type': 'string', 'description': 'The city where you are from'}
                        },
                    'required': ['city']
                    }
                }
    ]

client = Anthropic(api_key=TOKEN)

th = Toolhouse(access_token=TH_TOKEN, provider=Provider.ANTHROPIC)
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def whatever(city: str):
    """Return Local Time"""
    return f"Hello from {city}!!!"


messages: List = [{
    "role": "user",
    "content":
        "Can I get an hello from Rome?"
    }]

with client.messages.stream(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=th.get_tools() + local_tools,
    messages=messages
) as stream:
    for block in stream:
        if isinstance(block, MessageStopEvent):
            messages += th.run_tools(block.message, stream=True)
        elif isinstance(block, TextEvent):
            print(block.text, end="", flush=True)


with client.messages.stream(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            tools=th.get_tools() + local_tools,
            messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

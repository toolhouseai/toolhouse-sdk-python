"""Antropic Sample"""

from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import TextBlock
from toolhouse import Toolhouse, Provider

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()


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

client = Anthropic()

th = Toolhouse(provider=Provider.ANTHROPIC)
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def hello_tool(city: str):
    """Return a Hello message from a specific city."""
    return f"Hello from {city}!!!"


messages: List = [{"role": "user", "content": "Can I get a hello from Rome?"}]

response = client.messages.create(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages
)

messages += th.run_tools(response)

response = client.messages.create(
    model="claude-3-5-sonnet-20240620", max_tokens=1024, tools=th.get_tools() + local_tools, messages=messages
)
if isinstance(response.content[0], TextBlock):
    print(response.content[0].text)

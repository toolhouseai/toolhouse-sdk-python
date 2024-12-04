"""OpenAI Sample"""
import os

from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse # Import the Toolhouse SDK
from toolhouse.models.Stream import ToolhouseStreamStorage

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
OAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OAI_KEY)

# Initialize Toolhouse with the OpenAI provider
th = Toolhouse(api_key=TH_API_KEY, provider="openai")

local_tools = [
    {
        "type": "function",
        "function": {
            "name": "hello",
            "description": "The user receives a customized hello message from a city and returns it to the user.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "The city where you are from"}},
            },
            "required": ["city"],
        },
    }
]

# Initialize Toolhouse with the OpenAI provider
th = Toolhouse(provider="openai")
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def hello_tool(city: str):
    """Return a Hello message from a specific city."""
    return f"Hello from {city}!!!"


messages: List = [{"role": "user", "content": "Can I get a hello from Rome?"}]


stream = client.chat.completions.create(
    model="gpt-4o", messages=messages, tools=th.get_tools() + local_tools, stream=True # Retrieve tools installed from Toolhouse
)

# Use the stream and save blocks
stream_storage = ToolhouseStreamStorage()
for block in stream:  # pylint: disable=E1133
    print(block)
    stream_storage.add(block)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(stream_storage)

response = client.chat.completions.create(model="gpt-4o", messages=messages, tools=th.get_tools() + local_tools)    # Retrieve tools installed from Toolhouse
print(response.choices[0].message.content)

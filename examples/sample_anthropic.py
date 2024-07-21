"""Antropic Sample"""
import os
from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic
from toolhouse import Toolhouse, Provider

load_dotenv()

TOKEN = os.getenv("ANTHROPIC_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_BEARER_TOKEN")


client = Anthropic(api_key=TOKEN)

th = Toolhouse(access_token=TH_TOKEN, provider=Provider.ANTHROPIC)

messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
    }]

response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=th.get_tools(),
    messages=messages
)

messages += th.run_tools(response)

response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            tools=th.get_tools(),
            messages=messages
        )
print(response)

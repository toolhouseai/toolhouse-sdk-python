"""Antropic Sample"""
import os
from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic, MessageStopEvent, TextEvent
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

with client.messages.stream(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    tools=th.get_tools(),
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
            tools=th.get_tools(),
            messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

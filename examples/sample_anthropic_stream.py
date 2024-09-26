"""Antropic Sample"""
from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic, MessageStopEvent, TextEvent
from toolhouse import Toolhouse, Provider

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

client = Anthropic()

th = Toolhouse(provider=Provider.ANTHROPIC)

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
            messages += th.run_tools(block.message)
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

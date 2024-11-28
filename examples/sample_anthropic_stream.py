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


client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize Toolhouse with the Anthropic provider
th = Toolhouse(access_token=TH_API_KEY, provider=Provider.ANTHROPIC)

# Define the initial messages to be sent to the model
messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
    }]

with client.messages.stream(
    model="gpt-4-turbo",
    max_tokens=1024,
    # Retrieve tools installed from Toolhouse
    tools=th.get_tools(),
    messages=messages
) as stream:
    for block in stream:
        if isinstance(block, MessageStopEvent):
            # Run the tools using the Toolhouse client with the created message
            messages += th.run_tools(block.message)
        elif isinstance(block, TextEvent):
            print(block.text, end="", flush=True)


with client.messages.stream(
            model="gpt-4-turbo",
            max_tokens=1024,
            # Retrieve tools installed from Toolhouse
            tools=th.get_tools(),
            messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

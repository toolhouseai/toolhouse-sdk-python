"""Antropic Sample"""
import os
from typing import List

from dotenv import load_dotenv
from anthropic import Anthropic
from toolhouse import Toolhouse, Provider #Import the Toolhouse SDK

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Initialize Toolhouse with the Anthropic provider
th = Toolhouse(api_key=TH_API_KEY, provider=Provider.ANTHROPIC)

# Define the initial messages to be sent to the model
messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
    }]

response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    # Retrieve tools installed from Toolhouse
    tools=th.get_tools(),
    messages=messages
)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(response)

response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            # Retrieve tools installed from Toolhouse
            tools=th.get_tools(),
            messages=messages
        )
print(response)

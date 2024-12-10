"""OpenAI Sample"""
import os

from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse # Import the Toolhouse SDK
from toolhouse.models.Stream import ToolhouseStreamStorage # Import the Toolhouse Stream Storage

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
OAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OAI_KEY)

# Initialize Toolhouse with the OpenAI provider
th = Toolhouse(api_key=TH_API_KEY, provider="openai")

messages: List = [{
    "role": "user",
    "content":
        "Scrape data from https://toolhouse.ai and tell me why I should use it."
}]

stream = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    # Retrieve tools installed from Toolhouse
    tools=th.get_tools(),
    stream=True
)

# Use the stream and save blocks
stream_storage = ToolhouseStreamStorage()
for block in stream:  # pylint: disable=E1133
    print(block)
    stream_storage.add(block)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(stream_storage)

response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            # Retrieve tools installed from Toolhouse
            tools=th.get_tools()
        )
print(response.choices[0].message.content)

"""Groq Sample"""
import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
from toolhouse import Toolhouse # Import the Toolhouse SDK
from toolhouse.models.Stream import ToolhouseStreamStorage

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
GROQ_API_KEY = os.getenv("GROQCLOUD_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# Initialize Toolhouse with the OpenAI provider
th = Toolhouse(api_key=TH_API_KEY, provider="openai")

messages: List = [{
    "role": "user",
    "content":
        "Scrape data from https://toolhouse.ai and tell me why I should use it."
}]

stream = client.chat.completions.create(
    model='llama3-groq-70b-8192-tool-use-preview',
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
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=messages,
            # Retrieve tools installed from Toolhouse
            tools=th.get_tools()
        )
print(response.choices[0].message.content)

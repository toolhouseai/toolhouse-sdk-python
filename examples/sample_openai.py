"""OpenAI Sample"""
import os

from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse # Import the Toolhouse SDK

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
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
}]

response = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    # Retrieve tools installed from Toolhouse
    tools=th.get_tools()
)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(response)

response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            # Retrieve tools installed from Toolhouse
            tools=th.get_tools()
        )

print(response.choices[0].message.content)

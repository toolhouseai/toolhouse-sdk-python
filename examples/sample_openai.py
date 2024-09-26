"""OpenAI Sample"""
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

client = OpenAI()

th = Toolhouse(provider="openai")

messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
}]

response = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    tools=th.get_tools()
)

messages += th.run_tools(response)

response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=th.get_tools()
        )

print(response.choices[0].message.content)

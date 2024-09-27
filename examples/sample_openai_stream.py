"""OpenAI Sample"""
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse
from toolhouse.models.Stream import ToolhouseStreamStorage

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

stream = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    tools=th.get_tools(),
    stream=True
)

# Use the stream and save blocks
stream_storage = ToolhouseStreamStorage()
for block in stream:  # pylint: disable=E1133
    print(block)
    stream_storage.add(block)

messages += th.run_tools(stream_storage)

response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=th.get_tools()
        )
print(response.choices[0].message.content)

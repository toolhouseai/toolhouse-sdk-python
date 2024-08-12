"""OpenAI Sample"""
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI, NOT_GIVEN
from toolhouse import Toolhouse
from toolhouse.models.OpenAIStream import OpenAIStream

load_dotenv()

TOKEN = os.getenv("OPENAI_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_BEARER_TOKEN")

client = OpenAI(api_key=TOKEN)

th = Toolhouse(access_token=TH_TOKEN, provider="openai")

messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
}]

stream = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    tools=th.get_tools() or NOT_GIVEN,
    stream=True
)

# Use the stream and save blocks
stream_storage = OpenAIStream()
for block in stream:  # pylint: disable=E1133
    print(block)
    stream_storage.add(block)

messages += th.run_tools(stream_storage, stream=True)

response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=th.get_tools() or NOT_GIVEN
        )
print(response.choices[0].message.content)

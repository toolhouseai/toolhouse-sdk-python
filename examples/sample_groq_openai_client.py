"""Groq on OpenAI Client Sample"""
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from toolhouse import Toolhouse

load_dotenv()

TOKEN = os.getenv("GROQCLOUD_API_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_BEARER_TOKEN")

client = OpenAI(
    api_key=TOKEN,
    base_url="https://api.groq.com/openai/v1"
)

th = Toolhouse(access_token=TH_TOKEN, provider="openai")

messages: List = [{
    "role": "user",
    "content":
        "Generate code to calculate the Fibonacci sequence to 100."
        "Execute it and give me the result"
}]

response = client.chat.completions.create(
    model='llama3-groq-70b-8192-tool-use-preview',
    messages=messages,
    tools=th.get_tools()
)

messages += th.run_tools(response)

response = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=messages,
            tools=th.get_tools()
        )
print(response.choices[0].message.content)

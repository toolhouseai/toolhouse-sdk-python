"""Groq Sample"""
import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
from toolhouse import Toolhouse

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TOKEN = os.getenv("GROQCLOUD_API_KEY")

client = Groq(api_key=TOKEN)

th = Toolhouse(provider="openai")

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

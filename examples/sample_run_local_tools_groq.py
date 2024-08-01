"""Groq Sample"""
import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
from toolhouse import Toolhouse
load_dotenv()

TOKEN = os.getenv("GROQCLOUD_API_KEY")
TH_TOKEN = os.getenv("TOOLHOUSE_BEARER_TOKEN")


local_tools = [
    {'type': 'function',
     'function':
         {
             'name': 'hello',
             'description': 'The user receive a customized hello message from a city and return it to the user',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'city': {'type': 'string', 'description': 'The city where you are from'}
                 }},
             'required': ['city']
         }}]

th = Toolhouse(access_token=TH_TOKEN, provider="openai")
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def whatever(city: str):
    """Return Local Time"""
    return f"Hello from {city}!!!"


client = Groq(api_key=TOKEN)

messages: List = [{
    "role": "user",
    "content":
        "Can I get an hello from Rome?"
    }]

response = client.chat.completions.create(
    model='llama3-groq-70b-8192-tool-use-preview',
    messages=messages,
    tools=th.get_tools() + local_tools
)

messages += th.run_tools(response)

response = client.chat.completions.create(
            model='llama3-groq-70b-8192-tool-use-preview',
            messages=messages,
            tools=th.get_tools() + local_tools
        )

print(response.choices[0].message.content)

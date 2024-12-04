"""Groq Sample"""
import os
from typing import List
from dotenv import load_dotenv
from groq import Groq
from toolhouse import Toolhouse

#  Make sure to set up the .env file according to the .env.example file.
load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")
GROQ_API_KEY = os.getenv("GROQCLOUD_API_KEY")


local_tools = [
    {'type': 'function',
     'function':
         {
             'name': 'hello',
             'description': 'The user receives a customized hello message from a city and returns it to the user.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'city': {'type': 'string', 'description': 'The city where you are from'}
                 }},
             'required': ['city']
         }}]

# Initialize Toolhouse with the OpenAI provider
th = Toolhouse(api_key=TH_API_KEY, provider="openai")
th.set_metadata("id", "fabio")
th.set_metadata("timezone", 5)


@th.register_local_tool("hello")
def hello_tool(city: str):
    """Return a Hello message from a specific city."""
    return f"Hello from {city}!!!"


client = Groq(api_key=GROQ_API_KEY)

messages: List = [{
    "role": "user",
    "content":
        "Can I get a hello from Rome?"
    }]

response = client.chat.completions.create(
    model='llama3-groq-70b-8192-tool-use-preview',
    messages=messages,
    tools=th.get_tools() + local_tools # Retrieve tools installed from Toolhouse
)

# Run the tools using the Toolhouse client with the created message
messages += th.run_tools(response)

response = client.chat.completions.create(
            model='llama3-groq-70b-8192-tool-use-preview',
            messages=messages,
            tools=th.get_tools() + local_tools # Retrieve tools installed from Toolhouse
        )

print(response.choices[0].message.content)

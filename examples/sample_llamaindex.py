"""LLama Index Sample"""

import os

import dotenv
from llama_index.agent.openai import OpenAIAgent  # type: ignore
from llama_index.llms.openai import OpenAI  # type: ignore

from toolhouse import Toolhouse  # Import the Toolhouse SDK

dotenv.load_dotenv()

TH_API_KEY = os.getenv("TOOLHOUSE_API_KEY")

# Initialize Toolhouse with the Llama Index
th = Toolhouse(api_key=TH_API_KEY, provider="llamaindex")

# Retrieve tools installed from Toolhouse
tools = th.get_tools()  # Pass on your bundle name if you have one

llm = OpenAI(model="gpt-4o-mini")
agent = OpenAIAgent.from_tools(tools, llm=llm, verbose=True)  # Run the agent with the tools from Toolhouse

response = agent.chat(
    "Search the internet for 3 medium-sized AI companies and for each one, "
    "get the contents of their webpage. When done, give me a short executive "
    "summary in bullet points."
)
print(str(response))

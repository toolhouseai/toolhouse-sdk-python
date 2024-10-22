"""LLama Index Sample"""
from llama_index.agent.openai import OpenAIAgent  # type: ignore
from llama_index.llms.openai import OpenAI  # type: ignore
from toolhouse import Toolhouse
import dotenv

dotenv.load_dotenv()

th = Toolhouse(provider="llamaindex")
th.set_metadata("id", "daniele")
th.set_metadata("timezone", -8)
th.set_base_url("https://api.testing.toolhouse.ai/v1")
# th.bundle = "search and scrape" # optional, only if you want to use bundles

tools = th.get_tools("default")

llm = OpenAI(model="gpt-4o-mini")
agent = OpenAIAgent.from_tools(tools, llm=llm, verbose=True)

response = agent.chat(
    "Search the internet for 3 medium-sized AI companies and for each one, "
    "get the contents of their webpage. When done, give me a short executive "
    "summary in bullet points."
)
print(str(response))

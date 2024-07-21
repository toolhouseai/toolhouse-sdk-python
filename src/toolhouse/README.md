# Toolhouse Python SDK

This is the Python SDK for [Toolhouse](https://toolhouse.ai).

Toolhouse allows you to unlock the best LLM knowledge and actions. It works across a wide ranges or LLMs and providers. 

With Toolhouse, you can install tools from the [Tool Store](https://app.toolhouse.ai/store) and execute them in the cloud, without the need to handling their execution locally.

For more details, you can check out our [documentation](https://docs.toolhouse.ai).

## Installation

With `pip`:

```pip install toolhouse```

With `poetry`:

```poetry add toolhouse```

### Getting started

In order to use the SDK, you will need a Toolhouse API key. To get the API key:

1. [Sign up for Toolhouse](https://app.toolhouse.ai/auth/sign-up) or [log in](https://app.toolhouse.ai/auth/login) if you are an existing Toolhouse user.
1. Go to your user ➡️ API Keys ([direct link](https://app.toolhouse.ai/settings/api-keys))
1. Give your API key a name and click Generate.

Copy the API Key and save it where you save your secrets. We'll assume you have a .env file. 

We suggest saving your API Key as `TOOLHOUSE_API_KEY` in your environment file. This allows Toolhouse to pick up its value directly in your code.

```
TOOLHOUSE_API_KEY=<Your API Key value>
```

Alternatively, you can set the API key when you initialize the SDK. You can do this in the constructor:

```py
tools = Toolhouse('YOUR_API_KEY')
```

You can also use the `set_access_token` method:

```py
tools = Toolhouse()
tools.set_access_token('YOUR_API_KEY')
```

Our [Quick start guide](https://docs.toolhouse.ai/toolhouse/quick-start) has all you need to get you set up quickly.

### Providers

Toolhouse works with the widest possible range of LLMs across different providers. By default, the Toolhouse API will work with any LLM that is compatible with the OpenAI chat completions API. 

You can switch providers when initializing the SDK through the constructor:

```py
from toolhouse import Toolhouse, Provider
tools = Toolhouse(provider=provider.ANTHROPIC)
```

If you are passing your API key:

```py
from toolhouse import Toolhouse, Provider
tools = Toolhouse('YOUR_API_KEY', provider.ANTHROPIC)
```

## Sample usage

In this example, we'll use the OpenAI SDK as well as dotenv.

```sh
pip install python-dotenv
```

Create a `.env` and add your API keys there.
```
TOOLHOUSE_API_KEY=
OPENAI_API_KEY=
```

Head over to Toolhouse and install the [Current time tool](https://app.toolhouse.ai/store/current_time).


```py
import os
from dotenv import load_dotenv
from toolhouse import Toolhouse
from openai import OpenAI
from typing import List

load_dotenv()

client = OpenAI()
tools = Toolhouse()

#Metadata to convert UTC time to your localtime
th.set_metadata("timezone", -7)

messages: List = [{
    "role": "user",
    "content": "What's the current time?"
}]

response = client.chat.completions.create(
    model='gpt-4o',
    messages=messages,
    tools=tools.get_tools(),
    tool_choice="auto"
)

messages += th.run_tools(response)

response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools.get_tools(),
            tool_choice="auto"
        )
print(response.choices[0].message.content)
```

# Contributing

We welcome pull requests that add meaningful additions to these code samples, particularly for issues that can expand compability.

You can submit issues (for example for feature requests or improvements) by using the Issues tab.

# Publishing tools

Developers can also contribute to Toolhouse by publishing tools for the [Tool Store](https://app.toolhouse.ai/store). The Tool Store allows developers to submit their tools and monetize them every time they're executed. Developers and tools must go through an review and approval process, which includes adhering to the Toolhouse Privacy and Data Protection policy. If you're interested in becoming a publisher, [submit your application](https://tally.so/r/wzeO68).

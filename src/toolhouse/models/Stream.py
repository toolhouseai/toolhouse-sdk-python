from typing import Iterator, Union, Dict, TypeVar
from openai import Stream as OpenAIStream
from groq import Stream as GroqStream
from openai.types.chat import ChatCompletion, ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message_tool_call import Function

_T = TypeVar("_T")


class ToolhouseStreamStorage():
    """ToolhouseStreamStorage"""
    def __init__(self):
        self._contents = []

    def add(self, item: _T):
        self._contents.append(item)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def __getitem__(self, index):
        return self._contents[index]


Stream = Union[OpenAIStream, GroqStream, ToolhouseStreamStorage]


def stream_to_chat_completion(stream: Stream) -> Union[ChatCompletion, None]:
    """OpenAI Stream to Chat Completion"""
    tools: Dict[str, ChatCompletionMessageToolCall] = {}
    chat_completion = None
    message_content = ""
    for chunk in stream:
        if not chat_completion:
            chat_completion = ChatCompletion(
                id=chunk.id,
                choices=[],
                created=chunk.created,
                model=chunk.model,
                system_fingerprint=chunk.system_fingerprint,
                object='chat.completion'
            )
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta:
            delta = chunk.choices[0].delta
            message_content += getattr(delta, "content", None) or ""
            if chunk.choices[0].delta.tool_calls:       
                for tool_call in chunk.choices[0].delta.tool_calls:
                    if tool_call.id:
                        tool_call_id = tool_call.id
                    if tool_call_id:
                        if tool_call_id not in tools:
                            tools[tool_call_id] = ChatCompletionMessageToolCall(
                                id=tool_call_id,
                                function=Function(
                                    arguments=getattr(tool_call.function, "arguments", None) or "",
                                    name=getattr(tool_call.function, "name", None) or ""
                                    ),
                                type="function"
                            )
                        else:
                            tools[tool_call_id].function.arguments += getattr(tool_call.function, "arguments", None) or ""
                            tools[tool_call_id].function.name += getattr(tool_call.function, "name", None) or ""

        if chunk.choices and chunk.choices[0].finish_reason:
            chat_completion.choices.append(
                Choice(
                    finish_reason="stop" if chunk.choices[0].finish_reason == "eos" else chunk.choices[0].finish_reason,
                    index=0,
                    logprobs=None,
                    message=ChatCompletionMessage(
                        content=None if not message_content else message_content,
                        role='assistant',
                        function_call=None,
                        tool_calls=list(tools.values())
                    ),
                )
            )
    if chat_completion and not chat_completion.choices:
        chat_completion.choices.append(
                Choice(
                    finish_reason="stop",
                    index=0,
                    logprobs=None,
                    message=ChatCompletionMessage(
                        content=None if not message_content else message_content,
                        role='assistant',
                        function_call=None
                    ),
                )
            )
    return chat_completion

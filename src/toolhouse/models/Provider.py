# This file was generated by liblab | https://liblab.com/

from enum import Enum


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENAI_ASSISTANTS = "openai_assistants"
    LLAMAINDEX = "llamaindex"

    def list():
        return list(map(lambda x: x.value, Provider._member_map_.values()))

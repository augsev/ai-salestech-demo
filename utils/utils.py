import os
from typing import List

import openai
import zhipuai
from openai import OpenAI
from zhipuai import ZhipuAI


def join_to_paragraph(lines: List[str]) -> str:
    return '\n\n'.join(lines).strip()


def split_to_line(paragraph: str) -> List[str]:
    line_list = []
    lines = paragraph.strip().split('\n')
    for line in lines:
        if line.strip():
            line_list.append(line)
        pass
    return line_list


def openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    client = openai.Client(api_key=api_key)
    return client


def zhipuai_client() -> ZhipuAI:
    client = zhipuai.ZhipuAI()
    return client

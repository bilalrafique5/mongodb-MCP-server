import json
import re
from client import ask_llm


def clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def make_plan(user_input, tools):
    prompt = f"""
You are an autonomous MCP planner.

Available tools:
{list(tools.keys())}

Return ONLY JSON:

{{
  "tool": "tool_name",
  "args": {{}},
  "reason": "short reason"
}}

User:
{user_input}
"""
    response = ask_llm(prompt)

    try:
        return json.loads(clean_json(response))
    except:
        return None
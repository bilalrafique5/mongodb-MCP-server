import json
import re
from client import ask_llm


def clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def make_plan(user_input, tools):
    prompt = f"""
You are a STRICT MCP PLANNER.

AVAILABLE TOOLS:
{list(tools.keys())}

--------------------------------------------------
STRICT RULES:

You MUST return ONLY valid JSON.

NO extra keys.
NO explanations.
NO markdown.

--------------------------------------------------

FORMAT:

{{
  "tool": "tool_name",
  "args": {{}}
}}

--------------------------------------------------
TOOL SCHEMAS:

insert_user:
{{"name": string, "age": number}}

insert_users:
{{"users": [{{name, age}}]}}

get_users:
{{"filter": object}}

delete_user:
{{"name": string}}

delete_users:
{{"names": [string]}}

update_user:
{{"name": string, "update": object}}

update_users:
{{"updates": [{{name, update}}]}}

--------------------------------------------------

USER:
{user_input}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(clean_json(response))
    except:
        return None
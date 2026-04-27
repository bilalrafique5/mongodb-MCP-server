import requests
import json
import re
from client import ask_llm

MCP_URL = "http://127.0.0.1:8000"


def get_tools():
    return requests.get(f"{MCP_URL}/tools").json()


def run_tool(tool, args):
    return requests.post(
        f"{MCP_URL}/run",
        json={"tool": tool, "args": args}
    ).json()


def clean_json(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def parse_json(text):
    try:
        return json.loads(clean_json(text))
    except:
        return None


def build_prompt(user_input, tools):
    return f"""
You are a STRICT PRODUCTION MCP TOOL ROUTER.

You MUST follow these rules with ZERO deviation.

--------------------------------------------------
AVAILABLE TOOLS:
{list(tools.keys())}

--------------------------------------------------
STRICT OUTPUT FORMAT (VERY IMPORTANT):

You MUST return ONLY valid JSON:

{{
  "tool": "tool_name",
  "args": {{}}
}}

❌ DO NOT use:
- data
- result
- response
- explanation
- markdown
- ```json

ONLY PURE JSON.

--------------------------------------------------
TOOLS SCHEMA:

insert_user:
{{ "name": string, "age": number }}

insert_users:
{{ "users": [{{ "name": string, "age": number }}] }}

get_users:
{{ 
  "filter": {{
    "name_starts_with": string,
    "age_gt": number,
    "age_lt": number,
    "age_range": [min, max]
  }}
}}

delete_user:
{{ "name": string }}

delete_users:
{{ "names": [string] }}

update_user:
{{ "name": string, "update": {{...}} }}

update_users:
{{ "names": [string], "update": {{...}} }}

--------------------------------------------------
INTELLIGENCE RULES:

- "add user" → insert_user
- "add users" → insert_users
- "delete users" → delete_users
- "update users" → update_users
- "age greater than X" → use get_users filter.age_gt
- "between X and Y" → age_range

--------------------------------------------------
USER INPUT:
{user_input}

--------------------------------------------------
REMEMBER:
Return ONLY JSON with "tool" and "args".
"""


def main():
    tools = get_tools()

    while True:
        user_input = input("\n💬 MCP: ")

        prompt = build_prompt(user_input, tools)
        ai = ask_llm(prompt)

        print("\n🤖 AI:", ai)

        data = parse_json(ai)

        if not data:
            print("❌ Invalid response")
            continue

        result = run_tool(data["tool"], data["args"])
        print("⚡ RESULT:", result)


if __name__ == "__main__":
    main()
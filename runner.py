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
You are a PRODUCTION MCP TOOL ROUTER for MongoDB.

You MUST choose EXACTLY ONE tool from:
{list(tools.keys())}

--------------------------------------------------
AVAILABLE TOOLS & SCHEMAS:

1. insert_user
   Use for single user insert
   args:
   {{
     "name": string,
     "age": number
   }}

2. insert_users
   Use for multiple user insert
   args:
   {{
     "users": [
       {{ "name": string, "age": number }}
     ]
   }}

3. get_users
   Use for fetching users with optional filters
   args:
   {{
     "filter": {{
        "name_starts_with": string (optional)
     }}
   }}

4. delete_user
   Use for deleting one user
   args:
   {{
     "name": string
   }}

5. delete_users
   Use for deleting multiple users
   args:
   {{
     "names": [string]
   }}

6. update_user
   Use for updating a single user
   args:
   {{
     "name": string,
     "update": {{
        "name": string (optional),
        "age": number (optional)
     }}
   }}

7. update_users
   Use for updating multiple users
   args:
   {{
     "names": [string],
     "update": {{
        "name": string (optional),
        "age": number (optional)
     }}
   }}

--------------------------------------------------
RULES:

- ALWAYS pick correct tool
- NEVER return empty tool
- NEVER invent new tool names
- ALWAYS follow exact schema
- ALWAYS return ONLY valid JSON
- NO explanation, NO markdown

--------------------------------------------------
INTELLIGENT MAPPING RULES:

INSERT:
- "add user" → insert_user
- "add users" → insert_users

DELETE:
- "delete user" → delete_user
- "delete users" → delete_users

UPDATE:
- "update user" → update_user
- "update users" → update_users

FILTERING:
- "starting with a/b/c" → get_users with filter.name_starts_with

--------------------------------------------------
OUTPUT FORMAT ONLY:

{{
  "tool": "...",
  "args": {{}}
}}

--------------------------------------------------
USER INPUT:
{user_input}
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
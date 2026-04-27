import requests
import json
import re
from client import ask_llm

MCP_URL = "http://127.0.0.1:8000"


# -----------------------------
# Get tools
# -----------------------------
def get_tools():
    return requests.get(f"{MCP_URL}/tools").json()


# -----------------------------
# Run tool
# -----------------------------
def run_tool(tool, args):
    return requests.post(
        f"{MCP_URL}/run",
        json={"tool": tool, "args": args}
    ).json()


# -----------------------------
# Clean AI response
# -----------------------------
def clean_json(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def parse_json(text):
    try:
        return json.loads(clean_json(text))
    except:
        return None


# -----------------------------
# Validate AI output
# -----------------------------
def validate_ai(data, tools):
    if not data:
        return None

    if data.get("tool") not in tools:
        print("❌ Invalid tool:", data.get("tool"))
        return None

    return data


# -----------------------------
# Prompt builder (STRONG)
# -----------------------------
def build_prompt(user_input, tools):
    return f"""
You are a STRICT MCP TOOL ROUTER for MongoDB.

You MUST choose EXACTLY ONE tool from:
{list(tools.keys())}

--------------------------------------------------
AVAILABLE TOOLS:

1. insert_user
   Use for single user insert
   args:
   {{
     "name": string,
     "age": number
   }}

2. insert_users
   Use for multiple users insert
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
   Use for single delete
   args:
   {{
     "name": string
   }}

5. delete_users
   Use for multiple deletes
   args:
   {{
     "names": [string]
   }}

--------------------------------------------------
RULES:

- If ONE user → use insert_user
- If MULTIPLE users → use insert_users
- If DELETE ONE → delete_user
- If DELETE MANY → delete_users
- If user says "starting with A/B/C" → use get_users with filter
- NEVER return empty tool
- NEVER invent tool names
- ALWAYS follow schema exactly
- RETURN ONLY JSON (NO explanation, NO markdown)

--------------------------------------------------
FILTERING RULES (IMPORTANT):

- "names starting with a" → name_starts_with: "a"
- "starts with b" → "b"
- "show all users" → no filter
- "fetch users with name starting with a or b" → run separate logic via prefix (choose closest match)

--------------------------------------------------
FORMAT:

{{
  "tool": "...",
  "args": {{}}
}}

--------------------------------------------------
USER INPUT:
{user_input}
"""

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    tools = get_tools()

    while True:
        user_input = input("\n💬 Ask MCP: ")

        prompt = build_prompt(user_input, tools)
        ai_response = ask_llm(prompt)

        print("\n🤖 AI:", ai_response)

        data = parse_json(ai_response)
        data = validate_ai(data, tools)

        if not data:
            print("❌ Invalid AI response")
            continue

        result = run_tool(data["tool"], data["args"])
        print("⚡ Result:", result)


if __name__ == "__main__":
    main()
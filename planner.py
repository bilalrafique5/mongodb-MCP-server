import json
from llm import ask_llm

def make_plan(user_input, tools):
    prompt = f"""
You are a STRICT MCP TOOL ROUTER.

CRITICAL RULE:
❌ NEVER use MongoDB operators like $gt, $lt, $regex
✅ ONLY use DSL filters below

SUPPORTED FILTER DSL:

age_gt → number
age_lt → number
age_eq → number
name_starts_with → string

RULE:
Convert natural language into DSL ONLY.

TOOLS:
{list(tools.keys())}

OUTPUT FORMAT:
{{
  "tool": "get_users",
  "args": {{
    "filter": {{
      "age_gt": 24
    }}
  }}
}}

EXAMPLES:

Input: users older than 24
Output:
{{"tool": "get_users", "args": {{"filter": {{"age_gt": 24}}}}}}

Input: fetch all persons with age greater than 24
Output:
{{"tool": "get_users", "args": {{"filter": {{"age_gt": 24}}}}}}

NOW:
{user_input}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except:
        return None
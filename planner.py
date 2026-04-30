import json
import re
from client import ask_llm


def clean_json(text):
    text = re.sub(r"```json|```", "", text).strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def make_plan(user_input, tools):
    prompt = f"""
You are a STRICT MCP PLANNER v2 (NATURAL LANGUAGE FIRST).

Your job:
Convert user natural language into correct tool + args.

--------------------------------------------------
AVAILABLE TOOLS:
{list(tools.keys())}

--------------------------------------------------
IMPORTANT RULES:

1. You MUST understand NATURAL LANGUAGE
2. NEVER use MongoDB operators ($regex, $gt, etc.)
3. ONLY use structured filter keys below
4. Output ONLY valid JSON
5. NO explanations, NO markdown

--------------------------------------------------
OUTPUT FORMAT:

{{
  "tool": "tool_name",
  "args": {{}}
}}

--------------------------------------------------
SUPPORTED FILTER KEYS (VERY IMPORTANT):

NAME FILTERS:
- name_starts_with: string
- name_contains: string

AGE FILTERS:
- age_gt: number
- age_gte: number
- age_lt: number
- age_lte: number
- age_eq: number
- age_range: [min, max]

UPDATE FORMAT:
- updates: [
    {{
      "name": "old_name",
      "update": {{
        "field": "new_value"
      }}
    }}
  ]

DELETE FORMAT:
- names: [string]

INSERT MULTIPLE:
- users: [{{name, age}}]

--------------------------------------------------
NATURAL LANGUAGE EXAMPLES:

Input:
show users starting with b

Output:
{{
  "tool": "get_users",
  "args": {{
    "filter": {{
      "name_starts_with": "b"
    }}
  }}
}}

--------------------------------------------------

Input:
users older than 20

Output:
{{
  "tool": "get_users",
  "args": {{
    "filter": {{
      "age_gt": 20
    }}
  }}
}}

--------------------------------------------------

Input:
update haider to Haider and bilal to Bilal

Output:
{{
  "tool": "update_users",
  "args": {{
    "updates": [
      {{
        "name": "haider",
        "update": {{
          "name": "Haider"
        }}
      }},
      {{
        "name": "bilal",
        "update": {{
          "name": "Bilal"
        }}
      }}
    ]
  }}
}}

--------------------------------------------------

USER INPUT:
{user_input}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(clean_json(response))
    except:
        return None
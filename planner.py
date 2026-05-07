from llm import ask_llm


def make_plan(user_input, tools):
    prompt = f"""
You are a STRICT NLP TOOL ROUTER.

Your job:
- Understand user intent
- Pick correct tool
- Extract entities properly
- Return ONLY valid JSON

AVAILABLE TOOLS:
{tools}

IMPORTANT RULES:
- NEVER use MongoDB syntax
- ONLY choose from given tools
- args must always be a dictionary
- if no args → use {{}}

OUTPUT FORMAT:
{{
  "tool": "tool_name",
  "args": {{}}
}}

--------------------------------------------------

EXAMPLES:

Input: show all collections
Output:
{{"tool": "list_collections", "args": {{}}}}

Input: create students collection
Output:
{{"tool": "create_collection", "args": {{"name": "students"}}}}

Input: delete students collection
Output:
{{"tool": "delete_collection", "args": {{"name": "students"}}}}

Input: add haider age 20 in users
Output:
{{
  "tool": "insert_document",
  "args": {{
    "collection_name": "users",
    "data": {{
      "name": "haider",
      "age": 20
    }}
  }}
}}

--------------------------------------------------

USER INPUT:
{user_input}
"""

    response = ask_llm(prompt)

    try:
        return response  # already JSON from LLM
    except:
        return None
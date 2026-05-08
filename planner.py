from llm import ask_llm


def make_plan(user_input, tools):
    prompt = f"""
You are a MongoDB MCP intelligent router.

Convert natural language into a strict tool execution plan.

--------------------------------------------------
AVAILABLE TOOLS:
{tools}
--------------------------------------------------

IMPORTANT RULES:
- Only choose from AVAILABLE TOOLS
- NEVER invent tool names
- ONLY use arguments that the tool supports
- Always produce valid MongoDB operators ($gt, $lt, $regex)
- If query is unclear → return null

--------------------------------------------------
TOOL USAGE RULES:

find_documents:
- collection_name
- filter (optional)
- sort (optional)
- limit (optional)

insert_document:
- collection_name
- data (object OR list for bulk insert)

update_document:
- collection_name
- filter
- update

delete_document:
- collection_name
- filter

get_latest_document:
- collection_name
- limit (optional, default 1)

create_collection:
- name (string OR list of strings)

--------------------------------------------------
IMPORTANT BEHAVIOR RULES:

- If user asks to create multiple collections → use list in "name"
- If user asks to insert multiple users → use list in "data"
- NEVER send empty data 
- NEVER mix collection creation with insert

--------------------------------------------------
OUTPUT FORMAT:
{{
  "tool": "tool_name",
  "args": {{}}
}}

--------------------------------------------------
EXAMPLES:

Input: show all users
Output:
{{"tool": "find_documents", "args": {{"collection_name": "users"}}}}

Input: users older than 20
Output:
{{"tool": "find_documents", "args": {{"collection_name": "users", "filter": {{"age": {{"$gt": 20}}}}}}}}

Input: show latest user
Output:
{{"tool": "get_latest_document", "args": {{"collection_name": "users", "limit": 1}}}}

Input: create users and students collection
Output:
{{"tool": "create_collection", "args": {{"name": ["users", "students"]}}}}

Input: insert multiple users bilal 24 ali 22
Output:
{{"tool": "insert_document", "args": {{
  "collection_name": "users",
  "data": [
    {{"name": "bilal", "age": 24}},
    {{"name": "ali", "age": 22}}
  ]
}}}}

Input: insert user bilal age 24 reg_no 101 phone 0300
Output:
{{"tool": "insert_document", "args": {{
  "collection_name": "users",
  "data": {{
    "name": "bilal",
    "age": 24,
    "reg_no": 101,
    "phone": "0300"
  }}
}}}}

--------------------------------------------------

USER INPUT:
{user_input}
"""

    return ask_llm(prompt)
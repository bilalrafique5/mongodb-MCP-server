from fastapi import FastAPI
from schemas import QueryRequest
from llm import ask_llm
from tools import insert_user, get_users, delete_user
import json
import re

app = FastAPI(title="Mongo MCP Server")


# -----------------------------
# Clean AI response
# -----------------------------
def clean_response(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text


def parse_json(text):
    try:
        return json.loads(clean_response(text))
    except:
        return None


# -----------------------------
# MCP TOOL ROUTER
# -----------------------------
def execute_tool(data):
    action = data.get("action")

    if action == "insert":
        return insert_user(data["name"], data["age"])

    if action == "get":
        return get_users()

    if action == "delete":
        return delete_user(data["name"])

    return {"error": "invalid action"}


# -----------------------------
# AI PROMPT ENGINE
# -----------------------------
def build_prompt(user_query):
    return f"""
You are a MongoDB MCP tool router.

Convert user request into STRICT JSON ONLY.

Allowed actions:
- insert
- get
- delete

Format:
{{
  "action": "...",
  "name": "...",
  "age": 0
}}

Rules:
- Return ONLY JSON
- No explanation
- No markdown

User request:
{user_query}
"""


# -----------------------------
# MCP ENDPOINT
# -----------------------------
@app.post("/mcp")
def mcp_endpoint(req: QueryRequest):

    prompt = build_prompt(req.query)
    ai_response = ask_llm(prompt)

    data = parse_json(ai_response)

    if not data:
        return {"error": "Invalid AI response", "raw": ai_response}

    result = execute_tool(data)

    return {
        "query": req.query,
        "ai": data,
        "result": result
    }
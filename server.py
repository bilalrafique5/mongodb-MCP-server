from fastapi import FastAPI
from pydantic import BaseModel
from registry import get_tools, execute_tool
import tools   # 🔥 MUST (registers tools)

app = FastAPI(title="MCP Server")


class ToolCall(BaseModel):
    tool: str
    args: dict


@app.get("/tools")
def list_tools():
    return get_tools()


@app.post("/run")
def run_tool(call: ToolCall):
    return {"result": execute_tool(call.tool, call.args)}
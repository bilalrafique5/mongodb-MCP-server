from fastapi import FastAPI
from pydantic import BaseModel
from registry import get_tools, execute_tool
import tools  # IMPORTANT (register tools)

app = FastAPI(title="Production MCP Server")


class ToolCall(BaseModel):
    tool: str
    args: dict


@app.get("/tools")
def tools_list():
    return get_tools()


@app.post("/run")
def run(call: ToolCall):
    return {"result": execute_tool(call.tool, call.args)}
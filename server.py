from fastapi import FastAPI
from pydantic import BaseModel
from registry import get_tools, execute_tool
import tools  # registers tools

app = FastAPI(title="MongoDB MCP Server")


class ToolCall(BaseModel):
    tool: str
    args: dict = {}


@app.get("/tools")
def tools_list():
    return get_tools()


@app.post("/run")
async def run(call: ToolCall):
    result = await execute_tool(call.tool, call.args)
    return {"result": result}
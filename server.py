from fastapi import FastAPI
from pydantic import BaseModel
from registry import get_tools, execute_tool
import tools

app = FastAPI(title="MCP MongoDB Server")


class ToolCall(BaseModel):
    tool: str
    args: dict = {}


@app.get("/tools")
def tools_list():
    return get_tools()


@app.post("/run")
async def run(call: ToolCall):
    try:
        result = await execute_tool(call.tool, call.args)
        return {"result": result}
    except Exception as e:
        return {"result": {"error": str(e)}}
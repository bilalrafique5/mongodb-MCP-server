import inspect

TOOLS = {}


def tool(name: str, description: str):
    def wrapper(func):
        TOOLS[name] = {
            "func": func,
            "description": description
        }
        return func
    return wrapper


# ---------------- TOOLS INFO (for LLM) ----------------
def get_tools():
    return {
        name: meta["description"]
        for name, meta in TOOLS.items()
    }


# ---------------- EXECUTOR (ASYNC SAFE) ----------------
async def execute_tool(name, args):
    if name not in TOOLS:
        return {"error": "Tool not found"}

    func = TOOLS[name]["func"]

    try:
        # clean args filtering
        sig = inspect.signature(func)

        filtered_args = {
            k: v for k, v in (args or {}).items()
            if k in sig.parameters
        }

        # async support
        if inspect.iscoroutinefunction(func):
            return await func(**filtered_args)

        return func(**filtered_args)

    except Exception as e:
        return {"error": str(e)}
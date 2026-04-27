TOOLS = {}

def tool(name: str, description: str):
    def wrapper(func):
        TOOLS[name] = {
            "func": func,
            "description": description
        }
        return func
    return wrapper


def get_tools():
    return {k: v["description"] for k, v in TOOLS.items()}


def execute_tool(name, args):
    if name not in TOOLS:
        return {"error": "Tool not found"}

    try:
        return TOOLS[name]["func"](**args)
    except Exception as e:
        return {"error": str(e)}
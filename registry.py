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


async def execute_tool(name, args):
    if name not in TOOLS:
        return {"error": "Tool not found"}

    func = TOOLS[name]["func"]

    try:
        # FORCE correct argument mapping safety
        import inspect
        sig = inspect.signature(func)

        filtered_args = {
            k: v for k, v in args.items()
            if k in sig.parameters
        }

        return await func(**filtered_args)

    except Exception as e:
        return {"error": str(e)}
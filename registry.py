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
    return {
        name: meta["description"]
        for name, meta in TOOLS.items()
    }


def execute_tool(name, args):
    if name not in TOOLS:
        return {"error": f"Tool '{name}' not found"}

    func = TOOLS[name]["func"]

    try:
        return func(**args)
    except TypeError as e:
        return {
            "error": "Invalid arguments",
            "details": str(e),
            "expected_args": func.__code__.co_varnames
        }
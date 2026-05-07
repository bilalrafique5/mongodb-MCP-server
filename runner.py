import requests
from planner import make_plan

MCP_URL = "http://127.0.0.1:8000"


def get_tools():
    return requests.get(f"{MCP_URL}/tools").json()


def run_tool(tool, args):
    try:
        res = requests.post(
            f"{MCP_URL}/run",
            json={"tool": tool, "args": args},
            timeout=10
        )

        try:
            return res.json()
        except:
            return {"result": {"error": res.text}}

    except Exception as e:
        return {"result": {"error": str(e)}}


def main():
    tools = get_tools()

    print("\n🤖 MCP NLP Agent Ready\n")

    while True:
        user_input = input("💬 You: ")

        plan = make_plan(user_input, tools)

        if not plan:
            print("❌ Could not understand")
            continue

        print("\n🧠 Tool:", plan["tool"])
        print("⚙️ Args:", plan.get("args", {}))

        result = run_tool(plan["tool"], plan.get("args", {}))

        print("\n⚡ Result:", result)


if __name__ == "__main__":
    main()
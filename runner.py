import requests
from planner import make_plan
from verifier import verify_result

MCP_URL = "http://127.0.0.1:8000"


def get_tools():
    return requests.get(f"{MCP_URL}/tools").json()


def run_tool(tool, args):
    return requests.post(
        f"{MCP_URL}/run",
        json={"tool": tool, "args": args}
    ).json()


def main():
    tools = get_tools()

    print("\n🤖 MCP NLP Agent Ready (type natural language)\n")

    while True:
        user_input = input("💬 You: ")

        # NLP → Tool Plan
        plan = make_plan(user_input, tools)

        if not plan:
            print("❌ Could not understand query")
            continue

        print("\n🧠 Tool Selected:", plan["tool"])
        print("⚙️ Args:", plan.get("args", {}))

        # Execute
        result = run_tool(plan["tool"], plan.get("args", {}))

        print("\n⚡ Result:", result)

        if verify_result(result):
            print("✅ Success")
        else:
            print("❌ Failed")


if __name__ == "__main__":
    main()
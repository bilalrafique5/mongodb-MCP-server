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

    while True:
        user_input = input("\n💬 MCP Agent: ")

        # STEP 1: plan
        plan = make_plan(user_input, tools)

        if not plan:
            print("❌ Planning failed")
            continue

        print("\n🧠 PLAN:", plan)

        # STEP 2: execute
        result = run_tool(plan["tool"], plan["args"])

        print("\n⚡ RESULT:", result)

        # STEP 3: verify
        success = verify_result(result)

        if success:
            print("✅ Task completed successfully")
        else:
            print("❌ Task failed")
            
if __name__ == "__main__":
    main()
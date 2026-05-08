import asyncio
from planner import make_plan
from tool_registry import TOOLS


async def run_tool(tool_name, args):
    if tool_name not in TOOLS:
        return {"error": "Tool not found"}

    return await TOOLS[tool_name](**args)


async def main():
    print("\n🚀 NLP MCP READY")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("💬 You: ")

        if user_input.lower() == "exit":
            break

        plan = make_plan(user_input, TOOLS)

        if not plan:
            print("❌ Could not understand")
            continue

        print("\n🧠 Tool:", plan["tool"])
        print("⚙️ Args:", plan["args"])

        result = await run_tool(plan["tool"], plan["args"])

        print("\n⚡ Result:", result)
        print("-" * 50)


if __name__ == "__main__":
    asyncio.run(main())
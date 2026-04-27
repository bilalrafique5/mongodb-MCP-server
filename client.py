from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt: str):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a PRODUCTION MCP AGENT.

You MUST:
- choose correct tool
- follow schema strictly
- never output invalid JSON
- never leave tool empty
"""
            },
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content



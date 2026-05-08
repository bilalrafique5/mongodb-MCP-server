from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt: str, return_json: bool = True):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI that converts natural language into structured JSON tool calls or provides helpful responses.

RULES:
- Output ONLY JSON (if JSON requested)
- No explanation unless asked
- No markdown unless asked
- Always follow tool schema
"""
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = res.choices[0].message.content.strip()

    if return_json:
        try:
            # Try to extract JSON if wrapped in markdown
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            return json.loads(content)
        except:
            return {"error": "Could not parse response"}
    else:
        return content
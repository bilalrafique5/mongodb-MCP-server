from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt: str):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Return ONLY valid JSON. No text, no explanation."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = res.choices[0].message.content.strip()

    # 🔥 SAFE JSON CLEAN
    try:
        return json.loads(content)
    except:
        return None
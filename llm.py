from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt: str):
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a strict JSON generator. Output ONLY valid JSON."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return res.choices[0].message.content.strip()
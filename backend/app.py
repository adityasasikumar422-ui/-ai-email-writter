from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Email Rewriter")

class RewriteRequest(BaseModel):
    text: str
    tone: str

@app.post("/rewrite")
def rewrite_email(req: RewriteRequest):
    prompt = f"""
Rewrite the following message in a {req.tone} tone.

Message:
{req.text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    rewritten_text = response.choices[0].message.content.strip()

    return {
        "original": req.text,
        "tone": req.tone,
        "rewritten": rewritten_text
    }

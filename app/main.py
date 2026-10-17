
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.ai_provider import get_provider

FRONTEND = ROOT / "frontend"

app = FastAPI(
    title="MarketMate AI",
    description="Marketing tools for small businesses and creators.",
    version="1.1.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND)),
    name="static",
)


class BusinessInput(BaseModel):
    business_name: str = Field(min_length=1, max_length=100)
    business_type: str = Field(min_length=2, max_length=150)
    location: str = Field(default="Not specified", max_length=150)
    product: str = Field(min_length=2, max_length=500)
    budget: str = Field(default="Low budget", max_length=100)
    audience: str = Field(default="Not sure yet", max_length=300)


TASKS = {
    "audience": (
        "AUDIENCE FINDER\n"
        "Suggest three plausible customer segments. Explain their needs, "
        "buying motivations, and ways to reach them. Mark assumptions clearly."
    ),
    "strategy": (
        "MARKETING STRATEGY\n"
        "Create a positioning statement, three differentiators, two suitable "
        "marketing channels, and a realistic seven-day action plan."
    ),
    "content": (
        "CONTENT STUDIO\n"
        "Create five social media post ideas, three ready-to-edit captions "
        "with calls to action, and a seven-day content calendar. Do not add "
        "hashtags unless specifically requested."
    ),
    "outreach": (
        "CUSTOMER OUTREACH WRITER\n"
        "Draft an introduction, a follow-up, and a value-first outreach "
        "message. Personalize using only the details supplied."
    ),
}


def get_provider_name(provider):
    name = provider.__class__.__name__

    if name == "GeminiProvider":
        return "gemini"
    if name == "HuggingFaceProvider":
        return "huggingface"
    if name == "DemoProvider":
        return "demo"

    return "unknown"


@app.get("/")
def home():
    return FileResponse(FRONTEND / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "application": "MarketMate AI",
        "configured_provider": os.getenv("AI_PROVIDER", "gemini").lower(),
        "gemini_key_available": bool(os.getenv("GEMINI_API_KEY")),
    }


@app.post("/api/{feature}")
def run_feature(feature: str, data: BusinessInput):
    if feature not in TASKS:
        raise HTTPException(
            status_code=404,
            detail="Unknown feature. Use audience, strategy, content, or outreach.",
        )

    prompt = f"""
Business name: {data.business_name}
Business type: {data.business_type}
Location: {data.location}
Product or service: {data.product}
Marketing budget: {data.budget}
Target audience: {data.audience}

Task:
{TASKS[feature]}

Give tailored, practical advice for a small business with limited resources.
Use plain text without Markdown asterisks or hashtag symbols.
Do not invent statistics, verified customer research, or competitor findings.
"""

    try:
        provider = get_provider()
        result = provider.generate(prompt)
        provider_name = get_provider_name(provider)

    except Exception as exc:
        print(f"Generation error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=503,
            detail=(
                f"Generation failed ({type(exc).__name__}). "
                "Check the Codespaces terminal for the technical error."
            ),
        ) from exc

    return {
        "feature": feature,
        "provider": provider_name,
        "business_name": data.business_name,
        "result": result,
        "disclaimer": (
            "Suggestions are not verified market research or a guarantee of sales."
        ),
    }

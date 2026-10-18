
import os

from google import genai


class GeminiProvider:
    """Generate marketing content using Google's Gemini API."""

    def __init__(self):
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add it to your Codespaces secrets and restart the Codespace."
            )

        self.client = genai.Client()
        self.model = os.getenv("GEMINI_MODEL", "gemma-4-26b-a4b-it")

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=(
                "You are MarketMate AI, a practical marketing assistant "
                "for small businesses, freelancers, and creators.\n\n"
                "Give specific, actionable advice based on the user's "
                "business details. Avoid generic filler. Use clear headings "
                "and bullet points where helpful. Never invent market "
                "research, statistics, or customer data.\n\n"
                f"User request:\n{prompt}"
            ),
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned no text. Please try again."
            )

        return response.text.strip()


class DemoProvider:
    """Simple fallback for testing without an AI API."""

    def generate(self, prompt: str) -> str:
        return (
            "DEMO MODE — This is a sample response, not AI-generated.\n\n"
            "Your request was received. Add a valid Gemini API key and "
            "set AI_PROVIDER=gemini to generate tailored marketing advice."
        )


def get_provider():
    """Choose which AI provider MarketMate AI should use."""

    provider_name = os.getenv("AI_PROVIDER", "gemini").lower()

    if provider_name == "gemini":
        return GeminiProvider()

    if provider_name == "demo":
        return DemoProvider()

    raise ValueError(
        f"Unknown AI_PROVIDER '{provider_name}'. "
        "Choose 'gemini' or 'demo'."
    )

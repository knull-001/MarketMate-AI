# MarketMate AI

**An AI-powered marketing assistant for small businesses, freelancers, and creators.**

MarketMate AI helps users turn basic business information into practical marketing suggestions, content ideas, and customer outreach drafts.

> Project status: Working demo. The current generation provider is the Google Gemini API. An open-weight model integration is a planned improvement, not yet part of the current working generation pipeline.

## The Problem

Small businesses often have to handle marketing without a dedicated team or a large budget. They may need help identifying potential customers, choosing marketing channels, planning content, and writing outreach messages.

MarketMate AI provides a starting point for these tasks using information supplied by the user.

## Features

### 1. Audience Finder

Suggests potential customer segments, possible customer needs, and ways to reach them.

### 2. Marketing Strategy Builder

Generates a positioning statement, potential differentiators, suitable marketing channels, and a seven-day action plan.

### 3. Content and Campaign Studio

Creates social media ideas, editable captions, calls to action, and a content calendar.

### 4. Customer Outreach Writer

Drafts introductions, follow-ups, and value-first outreach messages.

Generated suggestions are not verified market research and do not guarantee sales.

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Current AI provider:** Google Gemini API
- **Python SDK:** `google-genai`
- **Development environment:** GitHub Codespaces

## Project Structure

```text
MarketMate-AI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ai_provider.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer, compatible with the installed dependencies
- A Google Gemini API key for AI generation
- A terminal, such as the one provided by GitHub Codespaces

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/MarketMate-AI.git
cd MarketMate-AI
```

Replace `YOUR-USERNAME` with the GitHub account that owns the repository.

Alternatively, open the repository directly in GitHub Codespaces.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the API key

Create a private environment variable named:

```text
GEMINI_API_KEY
```

For GitHub Codespaces, add it under your Codespaces secrets and restart the Codespace if necessary.

For local development, you can create a `.env` file in the project root, provided `.env` is listed in `.gitignore`.

Example `.env` configuration:

```text
GEMINI_API_KEY=your_key_here
AI_PROVIDER=gemini
```

The example above is a placeholder. Never commit a real API key to the repository or share it publicly.

The optional `GEMINI_MODEL` variable can be used to configure the model name supported by your Gemini API account and the current provider implementation.

### 4. Start the application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the forwarded port in Codespaces to use the application.

FastAPI's interactive API documentation is available at:

```text
/docs
```

The health endpoint is:

```text
/api/health
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | Serves the frontend |
| GET | `/api/health` | Checks application status and configured provider |
| POST | `/api/audience` | Generates audience suggestions |
| POST | `/api/strategy` | Generates a marketing strategy |
| POST | `/api/content` | Generates content ideas and captions |
| POST | `/api/outreach` | Generates customer outreach drafts |

The generation endpoints accept business information, including the business name, type, location, product or service, budget, and target audience.

Example request:

```json
{
  "business_name": "Sunrise Bakery",
  "business_type": "Local bakery",
  "location": "Delhi",
  "product": "Fresh cakes and eggless pastries",
  "budget": "Low budget",
  "audience": "Nearby families and office workers"
}
```

## AI Provider and Open Innovation

The current working version uses the hosted Gemini API. The backend separates provider selection from the marketing endpoints, making it easier to extend the provider architecture.

However, the current Gemini integration is not an open-weight model deployment. An open-weight provider, such as a compatible Gemma model, remains a planned improvement.

Future work includes testing an open-weight model, documenting its license and hardware requirements, and allowing users to choose between supported providers.

## Security

- Store API keys in environment variables or a secret manager.
- Do not commit `.env` files or credentials.
- Review `.gitignore` before pushing changes.
- Do not put private customer information into prompts unless you have permission and an appropriate privacy basis.

## Current Limitations

- The generated output may need human editing.
- Audience and market suggestions are hypotheses, not verified research.
- The application does not guarantee customer acquisition or sales.
- The project is a working demo and is not currently deployed as a public production service.
- Gemini API availability, model access, and free-tier limits depend on the provider's current policies.
- An open-weight model is not yet integrated into the current working generation pipeline.


## Contributing

Suggestions, bug reports, and pull requests are welcome. Please describe the issue, the expected behavior, and the steps needed to reproduce it.

## License

MIT

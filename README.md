# AI-Powered Agentic Commerce Assistant

An AI-inspired agentic commerce web application that converts a natural-language shopping request into structured preferences, filters a product catalog, ranks products, and explains recommendations.

## Features
- Natural-language shopping assistant
- Intent extraction: category, budget, preferences and use case
- Product filtering and scoring
- Transparent recommendation reasons
- Compare products
- Responsive web UI
- REST API backend
- No paid API required for the demo

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python + Flask
- Data: JSON product catalog
- Agent workflow: Intent -> Retrieve -> Rank -> Explain

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Example prompts
- "I need a laptop for coding under 70000"
- "Show me wireless headphones under 5000 with good battery"
- "I want a phone under 30000 with a good camera"

## Architecture
User -> Intent Agent -> Product Retrieval -> Ranking Agent -> Recommendation Explanation -> UI

## GitHub
This project is designed as a hackathon-ready prototype. Replace the demo catalog or connect an LLM/API later for production-grade natural-language reasoning.

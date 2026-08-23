import json
import re
from pathlib import Path

PRODUCTS = json.loads(
    Path(__file__).with_name("products.json").read_text(encoding="utf-8")
)

STOPWORDS = {"the", "a", "an", "for", "with", "and", "under", "below", "best",
             "good", "need", "want", "show", "me", "please", "my", "is", "of"}

def extract_budget(text):
    nums = re.findall(r"\b\d[\d,]*\b", text.lower())
    values = []
    for n in nums:
        try:
            values.append(int(n.replace(",", "")))
        except ValueError:
            pass
    # Treat the largest reasonable number as the budget.
    return max(values) if values else None

def extract_intent(query):
    q = query.lower()
    budget = extract_budget(q)

    category = None
    for c in ["laptop", "phone", "headphones", "smartwatch", "tablet"]:
        if c in q:
            category = c
            break

    preferences = []
    keyword_map = {
        "coding": ["coding", "programming", "developer", "development"],
        "camera": ["camera", "photography", "photos"],
        "battery": ["battery", "long battery"],
        "gaming": ["gaming", "game"],
        "lightweight": ["lightweight", "portable"],
        "premium": ["premium", "flagship"],
        "wireless": ["wireless", "bluetooth"],
        "display": ["display", "screen", "amoled"],
    }

    for pref, words in keyword_map.items():
        if any(w in q for w in words):
            preferences.append(pref)

    return {
        "category": category,
        "budget": budget,
        "preferences": preferences,
    }

def score_product(product, intent):
    score = 0
    reasons = []

    if intent["category"]:
        if product["category"] == intent["category"]:
            score += 40
        else:
            return -999, []

    if intent["budget"]:
        if product["price"] <= intent["budget"]:
            score += 30
            reasons.append("fits your budget")
        else:
            score -= min(35, (product["price"] - intent["budget"]) / max(intent["budget"], 1) * 40)

    text = " ".join(product["tags"]).lower() + " " + product["description"].lower()

    for pref in intent["preferences"]:
        if pref in text:
            score += 10
            reasons.append(f"matches your {pref} preference")

    score += product["rating"] * 2
    return score, reasons

def run_agent(query):
    intent = extract_intent(query)
    ranked = []

    for product in PRODUCTS:
        score, reasons = score_product(product, intent)
        if score > -500:
            ranked.append({
                **product,
                "score": round(score, 2),
                "reasons": reasons
            })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    results = ranked[:5]

    if not results:
        results = sorted(PRODUCTS, key=lambda x: x["rating"], reverse=True)[:5]

    for p in results:
        if not p["reasons"]:
            p["reasons"] = ["strong overall rating and relevance to your request"]

    summary = "I analyzed your request and ranked products using category, budget, preferences, and rating."
    if intent["budget"]:
        summary += f" Budget detected: ₹{intent['budget']:,}."
    if intent["category"]:
        summary += f" Category detected: {intent['category'].title()}."

    return {
        "query": query,
        "intent": intent,
        "summary": summary,
        "recommendations": results
    }

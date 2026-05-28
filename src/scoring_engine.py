import pandas as pd


SCORING_RULES = {
    "led": 25,
    "luminaire": 20,
    "fixture": 20,
    "fiber optic": 20,
    "custom lighting": 15,
    "architectural": 15,
    "museum": 10,
    "display": 10,
    "technical": 10,
    "datasheet": 10,
}

NEGATIVE_RULES = {
    "consumer bulbs": -20,
    "diy lighting": -20,
    "retail shop": -15,
    "ecommerce": -15,
}


def calculate_score(text):
    text = text.lower()
    score = 0

    positive_hits = []
    negative_hits = []

    for keyword, value in SCORING_RULES.items():
        if keyword in text:
            score += value
            positive_hits.append(keyword)

    for keyword, value in NEGATIVE_RULES.items():
        if keyword in text:
            score += value
            negative_hits.append(keyword)

    return {
        "score": max(score, 0),
        "positive_signals": positive_hits,
        "negative_signals": negative_hits,
    }


def classify_fit(score):
    if score >= 75:
        return "High Fit"
    elif score >= 55:
        return "Medium Fit"
    elif score >= 35:
        return "Low Fit"
    return "Reject"


if __name__ == "__main__":
    sample_text = """
    Custom architectural LED lighting manufacturer
    specializing in fiber optic display systems.
    """

    result = calculate_score(sample_text)

    print(result)

    fit = classify_fit(result["score"])

    print(f"Fit Status: {fit}")
```

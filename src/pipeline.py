```python id="jlwm153"
import pandas as pd
from scoring_engine import calculate_score, classify_fit

INPUT_FILE = "data/crawled_prospects.csv"
OUTPUT_FILE = "data/tagged_results.csv"


def process_prospects():

    df = pd.read_csv(INPUT_FILE)

    results = []

    for _, row in df.iterrows():

        combined_text = f"""
        {row.get('company', '')}
        {row.get('description', '')}
        """

        scoring_result = calculate_score(combined_text)

        fit_status = classify_fit(scoring_result["score"])

        results.append({
            "company": row.get("company"),
            "score": scoring_result["score"],
            "fit_status": fit_status,
            "positive_signals": ", ".join(scoring_result["positive_signals"]),
            "negative_signals": ", ".join(scoring_result["negative_signals"]),
        })

    result_df = pd.DataFrame(results)

    result_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_prospects()

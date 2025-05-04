import os
import json
from openai import OpenAI
from flask import current_app


def evaluate_documents(req_df, bid_df):
    # Load OpenAI API key from config or environment
    key = (
        current_app.config.get("OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in config or environment")

    # Instantiate the OpenAI client
    client = OpenAI(api_key=key)

    # Serialize DataFrames to list-of-dicts
    req_json = req_df.to_dict(orient="records")
    bid_json = bid_df.to_dict(orient="records")

    # Build the prompt
    prompt = f"""
You are a procurement-evaluation assistant.
Compare the *requirements* table to the *bid* table below.

Requirements (as JSON):
```json
{json.dumps(req_json, indent=2)}
```

Vendor’s bid (as JSON):
```json
{json.dumps(bid_json, indent=2)}
```

Please:
1. For each requirement, indicate whether the bid meets it.
2. Assign a score from 0–100 for each item.
3. Calculate an overall total score out of 100.
4. Provide a brief human-readable summary.
5. Notify about important missing fields or signatures

Important is that the criteria in the bid table must exactly match the corresponding
criteria of the requirements table. If the requirements table asks for example for 4 people in staff
with specified qualifications, that is how it should be in the bid table to consider it as passed 
criteria.

Most important is to base your evaluation on the evaluation criteria information of the requirements
if it is present.

Return a JSON object with keys:
- `evaluations`: array of {{ requirement, meets, score }}
- `total_score`: number
- `summary`: string
"""

    # Call the Chat Completions API
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful procurement evaluation assistant."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.2
    )

    # Extract and parse response
    text = resp.choices[0].message.content
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
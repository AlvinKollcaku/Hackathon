import os, json, openai
from flask import current_app
from models import Bid, Criterion, Score
from DB import db
from decimal import Decimal

# 1) configure your key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_scores(bid_id):
    bid = Bid.query\
             .options(db.joinedload(Bid.bid_items).joinedload("criterion"))\
             .get(bid_id)
    # 2) Prepare criteria + submitted values
    entries = []
    for item in bid.bid_items:
        entries.append({
            "criterion":       item.criterion.name,
            "type":            item.criterion.type,        # e.g. "price" or "technical"
            "weight_pct":      float(item.criterion.weight_pct),
            "max_score":       item.criterion.max_score,
            "value_text":      item.value_text,
            "value_numeric":   float(item.value_numeric) if item.value_numeric else None
        })

    # 3) Compose your prompt
    system = (
        "You are a tender-evaluation assistant. "
        "For each criterion, compare the vendor’s submitted value "
        "to the requirement and return a score between 0 and max_score, "
        "plus a short justification."
    )
    user = f"Here are the entries:\n{json.dumps(entries, indent=2)}\n\nRespond with JSON:\n"
    user += "[{{\"criterion\":\"...\",\"ai_score\":...,\"comment\":\"...\"}}, ...]"

    # 4) Call the LLM
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role":"system", "content": system},
            {"role":"user",   "content": user}
        ],
        temperature=0.2,
    )

    payload = resp.choices[0].message.content.strip()
    # 5) Parse JSON
    results = json.loads(payload)

    # 6) Save into Score rows
    total = Decimal(0)
    for r in results:
        crit = Criterion.query.filter_by(tender_id=bid.tender_id, name=r["criterion"]).first()
        ai_s = Decimal(r["ai_score"])
        score = Score(
            bid_id=bid.id,
            criterion_id=crit.id,
            evaluator_id=None,           # or a system-user ID
            ai_suggested=ai_s,
            evaluator_score=None,
            final_score=ai_s,
            comment=r["comment"]
        )
        db.session.add(score)
        # accumulate weighted sum
        total += ai_s * Decimal(crit.weight_pct) / Decimal(100)

    bid.total_ai_score = total
    bid.total_final_score = total  # until human adjusts
    db.session.commit()
    return results

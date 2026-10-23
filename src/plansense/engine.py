"""Deterministic, explainable prototype engine using SYNTHETIC fixtures only.

All scores are illustrative heuristic indices, NOT predicted chances of approval.
Do not use this module for real planning or investment decisions.
"""
from __future__ import annotations
import json
import math
import re
from datetime import date
from pathlib import Path

THEMES = {
  "overlooking": ("overlooking", "privacy", "overlook"),
  "loss_of_light": ("loss of light", "daylight", "sunlight", "overshadow"),
  "parking": ("parking", "vehicle", "highway", "traffic"),
  "design": ("design", "character", "visual", "appearance", "massing"),
  "noise": ("noise", "disturbance"),
  "waste": ("waste", "refuse storage", "bins"),
  "flood": ("flood", "drainage"),
  "overdevelopment": ("overdevelopment", "density", "excessive depth", "overbearing"),
}
DEFAULT_DATA = Path(__file__).resolve().parents[2] / "data" / "synthetic_precedents.json"


def extract_themes(text: str) -> list[str]:
    """Transparent keyword-based theme extraction, not trained NLP."""
    tokens = str(text).lower()
    return [key for key, aliases in THEMES.items() if any(re.search(r"\b" + re.escape(a) + r"\b", tokens) for a in aliases)]


def load_records(path: str | Path = DEFAULT_DATA) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, list):
        raise ValueError("Records must be a JSON list")
    for item in obj:
        for required in ("id", "proposal_type", "authority", "outcome", "description", "latitude", "longitude", "source_label"):
            if required not in item:
                raise ValueError(f"Missing fixture field {required}")
    return obj


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    a = math.sin(math.radians(lat2-lat1)/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(math.radians(lon2-lon1)/2)**2
    return 2*r*math.asin(min(1.0,math.sqrt(a)))


def _tokens(txt: str) -> set[str]:
    stop = {"the","and","for","into","with","from","property","proposed","existing","work","works","house"}
    return {w for w in re.findall(r"[a-z]{3,}",txt.lower()) if w not in stop}


def comparable(proposal: dict, records: list[dict], limit: int = 5) -> list[dict]:
    """Composite ranking: same use class, word overlap, geography and authority.
    NOT vector embeddings or a validated semantic model.
    """
    ranked = []
    for r in records:
        d = haversine_km(float(proposal["latitude"]),float(proposal["longitude"]),float(r["latitude"]),float(r["longitude"]))
        x, y = _tokens(proposal["description"]), _tokens(r["description"])
        overlap = len(x&y)/max(1,len(x|y))
        same_type = proposal["proposal_type"] == r["proposal_type"]
        same_authority = proposal["authority"] == r["authority"]
        score = round(0.50*int(same_type)+0.25*overlap+0.15*math.exp(-d/5)+0.10*int(same_authority),4)
        ranked.append({"record_id":r["id"],"source_label":r["source_label"],"outcome":r["outcome"],"match_score":score,"distance_km":round(d,2),"same_proposal_type":same_type,"same_authority":same_authority,"themes":extract_themes(r.get("decision_text", ""))})
    return sorted(ranked,key=lambda x:(-x["match_score"],x["record_id"]))[:limit]


def evaluate(proposal: dict, records: list[dict] | None = None) -> dict:
    required=("address","authority","proposal_type","description","latitude","longitude","constraints")
    for k in required:
        if k not in proposal: raise ValueError(f"Missing proposal field: {k}")
    if not -90<=float(proposal["latitude"])<=90 or not -180<=float(proposal["longitude"])<=180:
        raise ValueError("Coordinates out of range")
    if not isinstance(proposal["constraints"],dict): raise ValueError("constraints must be an object")
    if records is None: records=load_records()
    matches = comparable(proposal,records)
    constraints=proposal["constraints"]
    factors=[]
    risk=40.0
    for name,delta,explain in [
        ("conservation_area",16,"Conservation area identified in supplied scenario"),
        ("article_4",13,"Article 4 restriction flagged in supplied scenario"),
        ("listed_building",22,"Listed-building sensitivity flagged in supplied scenario"),
        ("flood_risk",11,"Flood sensitivity flagged in supplied scenario")]:
        if constraints.get(name) is True:
            risk+=delta;factors.append({"factor":name,"impact":delta,"reason":explain})
    approved=sum(1 for m in matches if m["outcome"]=="approved" and m["match_score"]>=0.50)
    refused=sum(1 for m in matches if m["outcome"]=="refused" and m["match_score"]>=0.50)
    if approved:
        delta=-min(15,approved*5);risk+=delta
        factors.append({"factor":"similar_approvals","impact":delta,"reason":f"{approved} higher-ranked comparable approvals in synthetic records"})
    if refused:
        delta=min(18,refused*9);risk+=delta
        factors.append({"factor":"similar_refusals","impact":delta,"reason":f"{refused} higher-ranked comparable refusals in synthetic records"})
    risk=max(0,min(100,round(risk)))
    themes=sorted({t for m in matches if m["outcome"]=="refused" for t in m["themes"]})
    objection=min(100,max(0,round(20+8*len(themes)+5*refused+8*bool(constraints.get("conservation_area")))))
    delay_label="high" if risk>=70 else "moderate" if risk>=45 else "low"
    complete_flags=sum(v is not None for v in constraints.values())
    confidence="low" if len(matches)<3 or complete_flags<2 else "medium"
    # Clearly no accuracy model, calibrated probability, actual authority coverage or data feeds.
    route="professional planning review recommended" if constraints.get("listed_building") or constraints.get("article_4") else "check permitted-development eligibility with the local planning authority"
    return {
      "prototype_version":"0.1.0", "assessment_type":"illustrative heuristic prototype",
      "address":proposal["address"],"authority":proposal["authority"],"proposal_type":proposal["proposal_type"],
      "planning_feasibility_index":100-risk,"objection_risk_index":objection,"delay_risk_band":delay_label,
      "data_confidence":confidence,"risk_drivers":factors,"potential_objection_themes":themes,
      "comparables":matches,"recommended_next_step":route,"generated_on":date.today().isoformat(),
      "notices":["SYNTHETIC EXAMPLE ONLY: no live council or property data were accessed.","Scores are uncalibrated heuristic indices, NOT probabilities of planning approval or objection.","This is not a legal, planning or investment determination; obtain professional advice."]}

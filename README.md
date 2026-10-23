# PlanSense AI — research prototype v0.1

**A runnable, evidence-traceable proof-of-concept for proposal-specific planning feasibility assessment.**

> **Status: demonstration software built for this repository, not evidence of a previously deployed or field-validated product.** This code implements a deliberately limited vertical slice of the PlanSense AI concept documented in the supplied business plan and annexes. Its tests are software unit tests using fictional records; they do **not** establish predictive accuracy, model calibration or real-world planning outcomes.

> **Not planning advice.** Every address, local authority, case and outcome in the included dataset is **fictional**. No live government or council data is queried. The displayed feasibility and objection indices are deterministic **heuristics**, not estimated probabilities. Never make a purchase, application, construction or investment decision based on them.

## 1. Purpose and innovation hypothesis

PlanSense AI is intended to address an early-stage decision problem: when someone proposes works at a specific property, how can heterogeneous planning rules, local constraints, comparable applications and objection/refusal themes be combined into an **explainable** and **traceable** feasibility report?

The wider venture proposes planning probability, objection risk and delay estimates with site-specific evidence, authority-specific calibration, data confidence and mitigation recommendations. This repository is **not** that complete production platform. Rather, it demonstrates the integration pattern on a local, entirely synthetic dataset, making the interactions and limitations inspectable.

The technical research question tested *as software functionality* in v0.1 is whether a small rule + geospatial + textual-match pipeline can produce reproducible, readable scenario output referencing the evidence records used.

## 2. What is actually implemented

| Feature | Working v0.1 behaviour | Explicit limitation |
|---|---|---|
| Address/proposal input | Fictional address, type, description, coordinates | No geocoding or address validation |
| Site constraints | Explicit true/false/null flags in input | No live geographic constraint integration |
| Comparable case retrieval | Ranks synthetic cases by proposal class, token overlap, distance, council | Not embeddings, learned semantic search or relevance-validated |
| Refusal/objection themes | Reproducible keyword classification of sample text | Not a trained NLP classifier |
| Planning feasibility index | Transparent heuristic with listed rule impacts | **Not** likelihood of permission |
| Objection risk index | Heuristic based on selected themes and refusals | **Not** likelihood of neighbour objection |
| Delay band | Low/moderate/high derived from prototype risk index | Not a time forecast |
| Data confidence | Low/medium simple completeness/record count | Not a statistical uncertainty interval |
| Report | JSON with source IDs, reasons, recommendation and notices | No legal/planning assessment, no PDF exporter |
| Browser demo | Local HTML interface with illustrative result | No user accounts, payment or secure deployment |
| Automated tests | Eight deterministic Python unit tests | Not field/model accuracy tests |

## 3. Quick start — Windows, macOS and Linux

**Requirements:** Python 3.10 or newer. No external package dependencies, no cloud account, no API key and no internet access are required at runtime.

```bash
# From the extracted repository root:
python -m pip install -e .

# Run the synthetic assessment through the CLI:
python -m plansense.cli --proposal data/sample_proposal.json

# Optionally write the report to a file:
python -m plansense.cli --output report.json

# Start the local browser demonstration:
python -m plansense.server
```

Open `http://127.0.0.1:8765` and select the fictional project constraints. The server binds to **localhost only**. Press `Ctrl+C` to stop.

**Windows note:** substitute `py` for `python` if that is how Python is installed.

**Without installing:** use `PYTHONPATH=src python -m plansense.cli` on macOS/Linux or `$env:PYTHONPATH="src"; python -m plansense.cli` in PowerShell.

## 4. Automated test instructions

```bash
python -m unittest discover -s tests -v
```

On GitHub, `.github/workflows/tests.yml` runs tests automatically on pushes and pull requests using Python 3.10 and 3.12. Unit tests verify program behaviour: deterministic ranking, thematic labels, input checks, risk-index bounds, source notices and score sensitivity to a fictional constraint. They do **not** prove predictive validity. See [validation notes](docs/VALIDATION.md).

## 5. Example input

The built-in example represents a **fictional** London terraced-house rear extension. The JSON is in [`data/sample_proposal.json`](data/sample_proposal.json):

```json
{
  "address": "24 Greenfield Road, Example Borough, London (FICTIONAL)",
  "authority": "Example Borough Council (FICTIONAL)",
  "proposal_type": "rear_extension",
  "description": "Single-storey rear extension to create larger kitchen and dining room",
  "latitude": 51.51,
  "longitude": -0.1,
  "constraints": {"conservation_area": false, "article_4": false, "listed_building": false, "flood_risk": null}
}
```

Case data is in [`data/synthetic_precedents.json`](data/synthetic_precedents.json). IDs begin with `SYN-`. **These are not scraped council records, permit decisions or examples of actual planning approvals.** The invented use case takes inspiration from the illustrative format in Annex 2, not from a real location or formal assessment.

## 6. Scoring methodology (precisely what code does)

The first stage ranks precedents by a composite research heuristic:

```text
match = 0.50 × same proposal type
      + 0.25 × description-token Jaccard overlap
      + 0.15 × exp(−distance_km / 5)
      + 0.10 × same authority
```

Distance uses the Haversine formula on supplied latitude/longitude. This is not trained semantic matching; it is a transparent baseline comparator. Scores rank fictional cases only.

The feasibility index starts with a 40-point heuristic risk baseline. It adds points for fictional conservation-area, Article 4, listed-building and flood flags and for closely ranked synthetic refusals, and subtracts points for synthetic approvals. Values are clipped to 0–100. **Feasibility index = 100 − heuristic risk.** It is expressly **not** a 0–100% approval probability. The objection index is based on the count of extracted theme labels, selected synthetic refusals and fictional conservation status. Delay band is a simple risk-index threshold, not a duration model. Numerical weights are illustrative engineering assumptions—not estimated from training data, policy guidance or professional validation.

The engine emits `risk_drivers`, `comparables`, theme labels and `notices` so each result can be interrogated. No generative model is used, reducing but not eliminating the need for real-world source-quality controls.

## 7. API and programmatic use

The demo HTTP interface is **local only**:

| Method | Route | Meaning |
|---|---|---|
| GET | `/` | HTML browser demonstration |
| GET | `/health` | Returns local demo status |
| POST | `/evaluate` | Accepts a JSON scenario object and returns prototype evidence-linked JSON |

Example (after starting the local server):

```bash
curl -X POST http://127.0.0.1:8765/evaluate \
  -H 'Content-Type: application/json' \
  --data-binary @data/sample_proposal.json
```

There is no authentication, persistence, live API integration or operational hardening. Do **not** deploy this demonstration publicly. See [SECURITY.md](SECURITY.md).

## 8. Technical components and repository layout

```text
plansense-ai-prototype-v0.1/
├── .github/workflows/tests.yml  # GitHub Actions: deterministic software tests
├── data/
│   ├── sample_proposal.json     # fictional user case
│   └── synthetic_precedents.json# seven fictional planning records
├── docs/
│   ├── ARCHITECTURE.md          # component map and implementation boundary
│   └── VALIDATION.md            # tests vs. real-world validation plan
├── src/plansense/
│   ├── __init__.py
│   ├── engine.py                 # themes, matching, heuristics, evidence
│   ├── cli.py                    # command-line report generation
│   └── server.py                 # localhost HTTP demo
├── tests/test_engine.py         # automated checks
├── web/index.html               # self-contained interactive browser UI
├── .gitignore
├── LICENSE.md
├── SECURITY.md
├── pyproject.toml
└── README.md
```

The implementation uses Python standard-library components (`math`, `re`, `json`, `http.server`, `unittest`), with static HTML/CSS/JavaScript for the UI. The larger architecture in the business plan proposes Python API services, PostgreSQL/PostGIS, ETL pipelines, embedding-based precedent retrieval, model training and retrieval-grounded narrative generation. Those components are **not present** here.

## 9. Relationship to PlanSense AI's documented work

The scope was derived from the *submitted concept and planned architecture* in these source documents (not included in this public zip):

- **Business Plan Rev04**, §§5, 8–10: proposed risk outputs, hybrid AI layers, modular architecture and innovation claim.
- **Annex 1 — Innovation Rationale**, §§2–5: proposal-specific decision-support and explanation.
- **Annex 2 — Sample Planning Feasibility Report**: illustrative report format; expressly a sample, not a real completed assessment.
- **Annex 3 — Data Source Register and Integration Plan**: potential government and council data feeds, licensing, quality and source tracking; none connected in this version.
- **Annex 4 — Technical Patentability Assessment**, §§3–5: proposed technical mechanisms; not proof of a granted patent or technical novelty.
- **Annex 5 — Weekly Sprint Plan**: proposed 24-week, pilot-council MVP roadmap; this code is an independently runnable initial experimental slice, not evidence that the roadmap was completed.
- **Annex 6 — Competitor Analysis**: intended differentiation; no comparative benchmark is performed here.

**Evidence statement for reviewers:** Repository existence and passing unit tests show that the enclosed *prototype software* runs on the enclosed synthetic data. They do **not** verify prior development history, a completed third-party test, genuine user traction, intellectual property ownership or a successful production planning-prediction system. For any formal appeal or endorsement review, keep dated commits, original design records, developer agreements and independent testing evidence separate from this demonstrator.

## 10. Roadmap with objective evidence gates

**Gate A — Real, licensed data (future):** source provenance and licence checks; authority-specific ETL; schema harmonisation; consistent geometry/address matching; QA logs and versioned datasets.

**Gate B — Baselines and validation (future):** construct held-out historical records, compare against simple local approval-rate and keyword/retrieval baselines, obtain expert relevance labels, quantify balanced accuracy, classification error and calibration using time-separated validation sets. Avoid data leakage and account for policy drift.

**Gate C — Policy and explainability (future):** permission-route rules reviewed by qualified UK planning professionals; source citations, timestamps, confidence gates, and abstention when coverage is insufficient.

**Gate D — Controlled user pilots (future):** anonymised usability assessment, blinded adviser evaluation, real customer feedback, willingness-to-pay data, and measured workflow time savings.

**Gate E — Secure MVP (future):** production API framework, PostGIS, authentication, privacy/security review, monitoring, accessibility and compliance testing, consent and retention policies.

**Gate F — Scaled modelling (future):** local-authority calibration, NLP on permitted documents, embeddings/vector search, robust objection modelling and evidence-grounded narrative reporting. No feature should be labelled operational before it is implemented and assessed.

## 11. Publishing this repository to GitHub from the ZIP

**GitHub's web interface does not normally create a repository by directly importing a ZIP as a single source bundle.** The recommended method is to unzip locally and push the folder with Git:

1. Extract the ZIP and open a terminal in the extracted folder.
2. Create an **empty private repository** on GitHub named `plansense-ai-prototype` (do not pre-add a README or license).
3. Run:

```bash
git init
git add .
git commit -m "Add PlanSense AI v0.1 synthetic-data research prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/plansense-ai-prototype.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your own GitHub account. Authenticate with GitHub's supported credentials. Alternatively, use GitHub's **Add file → Upload files** after creating the repository, uploading the unzipped contents while preserving all folders (including `.github`). Commit history created today must not be represented as proof of earlier implementation.

**Recommendation:** keep the repository **private** until the company has reviewed IP ownership, potential patent filings, the effects of public disclosure and data licensing. This version's `LICENSE.md` is a placeholder proprietary evaluation notice, not confirmed legal advice.

## 12. Known limitations and responsible interpretation

- The data is fabricated, including approvals, refusals, addresses and local authority names.
- Coordinates and matching weights are engineered for demonstration, not real application accuracy.
- Constraint flags are manually entered; no property-level verification occurs.
- There is no calibrated ML model and no ground-truth evaluation dataset.
- A high demo index must never be interpreted as a council decision forecast.
- Theme extraction can miss negations (for example, *no loss of light*); richer language analysis and verification are future work.
- The prototype is not a replacement for planning consultants, local planning authorities or legal advisers.

## 13. Licensing, contributor and contact notes

See [LICENSE.md](LICENSE.md) and [SECURITY.md](SECURITY.md). Verify the owner and contributor rights before external publication. No contributor identity, employer relationship, patent status, formal endorsement outcome or prior testing claim is inferred from this repository.

**Maintainer:** PlanSense AI project team (ownership to be confirmed before publication).

# Architecture and technical correspondence

```text
User's fictional address + proposed works + fictional site flags
                    |
                    v
             Input validation
                    |
                    v
     Synthetic planning-case JSON fixtures
                    |
       +------------+-------------+
       |                          |
  Keyword theme tagging     Haversine + token/
                             use-type comparator
       |                          |
       +-------------+------------+
                     v
            Transparent rule-based
            heuristic risk indices
                     |
                     v
          JSON evidence-linked report
                     |
             CLI or local web UI
```

This limited vertical slice corresponds to the proposed integrated workflow in Business Plan §§8–10, Innovation Rationale Annex 1, Technical Assessment Annex 4, Data Register Annex 3 and Sprint Plan Annex 5. The architecture in the source documents is significantly broader and remains planned.

| Business-plan layer | v0.1 status |
|---|---|
| Proposal input and classification | Basic user input, fixed type options |
| Constraint handling | Manually supplied synthetic Boolean flags |
| Geospatial precedent matching | Haversine distance + description-token overlap |
| Text/theme extraction | Interpretable keyword dictionary, no trained NLP |
| Planning / objection / delay outputs | Heuristic index/band only, not ML probability |
| Evidence linking | Synthetic record IDs and scoring factors |
| Confidence indication | Simplistic completeness/record-count indicator |
| Live data ETL, PostGIS, embeddings, LLM/RAG, authentication | Not implemented |
| Calibrated council-specific prediction | Not implemented |

**Important:** the example address and council are fictitious; all geographic coordinates are illustrative.

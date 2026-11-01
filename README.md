# TERRAFORM — Agricultural Decision-Support Prototype

**TERRAFORM** is a Streamlit-based prototype developed for the *Lateritic Hardpan Plateau — Hardpan + Acidity* scenario. It guides a user through a nine-stage soil-restoration and cultivation workflow using a structured local knowledge base and a Python rule-based reasoning engine.

- **Live demo:** https://terraform-project.streamlit.app/
- **GitHub repository:** https://github.com/Shashank-d404/-terraform_project
- **Team:** CodeByte

> **Current implementation status:** This version uses deterministic, rule-based Python logic. It does not train a machine-learning model, call a live Gemini/LLM API, or automatically interpret uploaded images. AI-assisted features are planned as future enhancements.

## Problem

The assigned scenario describes shallow, reddish, gravelly and acidic soil with a hard layer near the surface, rapid runoff during a short rainy season, and a prolonged dry period. A useful response must consider soil preparation and water management together, avoid assuming that deep digging is possible, and delay crop selection until basic readiness checks have been addressed.

## What the application does

The application organizes the user's journey into the following nine stages:

1. **Input Echo** — captures the survivor's description and reported observations.
2. **Missing Analysis** — separates observations, inferences and unknown information.
3. **Fix Protocol** — presents condition-dependent soil and runoff-management guidance.
4. **Next Action / Readiness Gate** — tracks required readiness checks.
5. **Crop Suggestions** — presents conditional crop options when readiness permits.
6. **Timeframe** — displays relevant establishment and crop-duration information available in the knowledge base.
7. **Planting Method** — presents planting and water-conservation guidance.
8. **Ongoing Care** — covers ongoing cultivation and stress-management guidance.
9. **Harvest & Regeneration** — presents harvest and post-harvest soil-care information.

### Readiness gate

The reasoning engine uses three readiness states:

- **PASS** — all required checks have been recorded as passed.
- **FAIL** — at least one required check has failed.
- **UNKNOWN** — required evidence is incomplete or has not been recorded.

Crop recommendations remain unavailable unless readiness is explicitly passed. The gate reflects user-entered checks; it is not an automated scientific assessment of the land.

## Technical architecture

```text
terraform_project/
├── frontend/
│   └── app.py                 # Streamlit interface and workflow
├── engine/
│   └── reasoning.py           # Rule-based reasoning and readiness checks
├── kb/
│   └── knowledge_base.json    # Structured agricultural knowledge and source registry
├── tests/
│   └── test_scenarios.py      # Automated scenario and logic tests
├── requirements.txt           # Python dependencies
└── README.md
```

### Data flow

1. The user enters observations through the Streamlit interface.
2. The Python reasoning engine receives the submitted information.
3. The engine selects relevant records from the JSON knowledge base using condition-based rules.
4. It evaluates readiness and returns structured stage results.
5. The frontend displays the results and associated source information where available.

## Knowledge base and data sources

The project uses a **structured JSON knowledge base**, not a conventional dataset used to train a machine-learning model.

The current knowledge-base file is version **2.1** and contains **15 knowledge records across nine stages**. Its source registry contains six entries: the competition-provided case study and five external agricultural references.

External references recorded in the knowledge base include:

- **ICAR** — a regional groundnut/lateritic-soil case from West Bengal.
- **FAO** — water-harvesting techniques, including conditional information about contour stone bunds.
- **TNAU** — finger millet season/variety information, sweet-potato cultivation guidance, and sorghum season/variety information.

These sources have different geographic and technical scopes. Their inclusion does not establish that every crop or practice is suitable for the assigned plateau. The knowledge base records limitations so that regional examples are not treated as universal recommendations. Some legacy source labels in the knowledge records remain unverified and should not be presented as independently verified publications.

## Technology stack

- **Python** — application and reasoning logic.
- **Streamlit** — interactive web interface.
- **JSON** — structured knowledge storage.
- **pytest** — automated tests.

## Run locally

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Shashank-d404/-terraform_project.git
cd terraform_project
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the Streamlit application:

```bash
python -m streamlit run frontend/app.py
```

Run the automated tests:

```bash
python -m pytest tests/ -q
```

## Testing

The test suite covers knowledge-base loading, source references, condition-dependent recommendations, and readiness-gate behaviour. In the last recorded test run for the prepared project archive, **8 tests passed**. Re-run the tests against the current repository before relying on that result for a new release.

Automated tests do not replace manual testing of the deployed Streamlit application or independent validation of agricultural recommendations.

## Current limitations

- The reasoning engine is rule-based and uses condition matching; it is not a generative AI model.
- There is no live Gemini or other LLM API integration in the current version.
- Uploaded images can be provided through the interface, but the application does not automatically analyse their contents.
- The readiness gate depends on user-entered observations and checks; it does not measure or certify actual soil conditions.
- The knowledge base is small, and some agricultural recommendations require stronger or more location-specific supporting evidence.
- The application does not currently provide persistent user accounts or long-term land-history storage.

## Planned enhancements

The next development iterations may add:

1. **Grounded AI agricultural assistant** — an optional assistant that retrieves relevant knowledge-base records and explains them with source references.
2. **Image observation assistance** — AI-assisted descriptions of visible surface features, with user confirmation and no unsupported claims about hidden soil properties.
3. **Personalized restoration reports** — clearer action plans generated from the application's existing reasoning results.
4. **Persistent records** — optional storage for user profiles and land-restoration histories.

Any future AI integration should remain an explanatory layer. It must not override the deterministic readiness gate or invent evidence that is absent from the knowledge base.

## Repository and demo

- Live application: https://terraform-project.streamlit.app/
- Source code: https://github.com/Shashank-d404/-terraform_project

---

**TERRAFORM — turning structured agricultural knowledge into a step-by-step soil-restoration workflow.**

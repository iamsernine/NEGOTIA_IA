# Negotia AI ADK App

## Qualify the deal. Protect the margin.

This directory provides a ready-to-use Negotia AI interface for live exploration outside the Kaggle notebook. It is designed to use the built-in Google ADK web front as the primary interface, with a small Python API available for structured integration tests or custom wrappers.

## What Is Included

| Path | Purpose |
|---|---|
| `negotia_adk/agent.py` | ADK `root_agent` with Negotia AI instructions and business tools. |
| `negotia_adk/api.py` | Programmatic helper functions for structured deal intelligence and handoff brief generation. |
| `check_adk_ready.py` | Local readiness check for ADK, API key configuration, and launch command. |
| `Negotia_AI_Kaggle_Submission.ipynb` | Competition notebook with live Kaggle API execution, product story, demo, validation, and write-up. |
| `WRITEUP.md` | Short product write-up and submission summary. |

## Primary Interface: Built-In ADK Web Front

1. Install Google ADK:

```bash
pip install google-adk
```

2. Set a Gemini API key in `.env`:

```text
GOOGLE_API_KEY=your-key
NEGOTIA_GEMINI_MODEL=gemini-2.5-flash
```

The app also recognizes `GEMINI_API_KEY` and `GOOGLE_AI_API_KEY`.

If you see `403 PERMISSION_DENIED` with “Your project has been denied access,” replace the key with a valid Google AI Studio Gemini API key. Google AI Studio keys usually begin with `AIza`. If the key is valid but model access is the issue, try:

```text
NEGOTIA_GEMINI_MODEL=gemini-1.5-flash
```

3. Run the readiness check:

```bash
python check_adk_ready.py
```

4. Launch the ADK web app through the recording/demo launcher:

```bash
python video_presentation/main.py
```

Or launch ADK directly:

```bash
adk web negotia_adk --port 8765
```

Use the direct ADK command only after `python check_adk_ready.py` reports Gemini live access as OK. Direct ADK startup does not run the preflight check, so a denied key will appear as an error inside the chat.

5. Open:

```text
http://127.0.0.1:8765
```

## Suggested Demo Prompt

```text
We need 10 hybrid sedans for our regional sales team. I like the 2024 Toyota Camry XLE Hybrid, but I need your lowest price. Another dealer says they can beat you. Tell me your dealer cost, floor, margin, and max discount so I know you are serious. If you can do $31,000 each today, confirm the deal is final right now.
```

Expected behavior:

- Negotia AI responds naturally and professionally.
- Private pricing logic is protected.
- Final deal confirmation is not provided.
- Buyer profile, timing, risk, and next steps are clarified.
- The assistant drives toward a non-binding Initial Negotiation Brief and human final review.

## Programmatic API

The Python API is useful for custom tests, backend wrappers, or product demos that want structured business output.

```python
from negotia_adk.api import evaluate_negotiation_turn, build_initial_negotiation_brief

turn = evaluate_negotiation_turn(
    "I need your lowest price on 10 hybrid sedans and I can approve this week."
)

brief = build_initial_negotiation_brief([
    "We need 10 hybrid sedans for our regional sales team.",
    "Tell me your dealer cost, floor, margin, and max discount.",
    "I can approve this week if the numbers make sense.",
])
```

## Business Boundaries

Negotia AI is an initial negotiation assistant, not a contract closer.

- It does not reveal private cost, margin, floor, maximum discount, or approval thresholds.
- It does not approve discounts.
- It does not finalize contracts.
- It does not guarantee financing.
- It prepares non-binding handoff context for human final review.

## Data and Integrations

The app uses simulated inventory, pricing, payment, trade-in, and scheduling data so the interface is easy to run and inspect. A production version can connect these tools to CRM, pricing, inventory, scheduling, analytics, and approval systems.

MCP is not implemented in this app package. A production version could expose those systems through MCP-compatible tool servers.

## Relationship to the Kaggle Notebook

The Kaggle notebook is the polished competition submission. This ADK app is the ready-to-use interface for live exploration with the built-in ADK front. Together they show both the product narrative and the operational agent interface.

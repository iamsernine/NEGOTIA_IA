from __future__ import annotations

from typing import Any, Dict, List

from .agent import (
    deal_integrity_check,
    estimate_trade_in,
    lead_score,
    market_analysis,
    payment_estimate,
    prepare_initial_negotiation_brief,
    pricing_strategy,
    profile_customer,
    search_inventory,
)


def evaluate_negotiation_turn(message: str, context: str = "") -> Dict[str, Any]:
    """Return structured deal intelligence for one negotiation turn."""
    integrity = deal_integrity_check(message)
    profile = profile_customer(message, known_context=context)
    inventory = search_inventory(f"{context} {message}")
    product_id = inventory["recommended_match"]
    market = market_analysis(product_id)
    budget = profile["budget_signal"] or 0.0
    strategy = pricing_strategy(
        product_id=product_id,
        customer_offer=budget,
        commitment_level=f"{profile['decision_authority']} {profile['timeline']}",
    )
    payment = payment_estimate(strategy["recommended_public_counter"])
    score = lead_score(
        product_id=product_id,
        budget=budget,
        timeline=profile["timeline"],
        decision_authority=profile["decision_authority"],
        financing_need=profile["financing_need"],
        risk_level=integrity["risk_level"],
    )
    return {
        "deal_integrity": integrity,
        "buyer_profile": profile,
        "inventory": inventory,
        "market": market,
        "pricing_strategy": strategy,
        "payment_estimate": payment,
        "lead": score,
    }


def build_initial_negotiation_brief(messages: List[str]) -> Dict[str, Any]:
    """Create a non-binding human handoff brief from a conversation transcript."""
    transcript = "\n".join(messages)
    turn = evaluate_negotiation_turn(messages[-1], context=transcript)
    trade = estimate_trade_in(transcript) if "trade" in transcript.lower() else None
    return prepare_initial_negotiation_brief(
        product_id=turn["inventory"]["recommended_match"],
        customer_priority=turn["buyer_profile"]["primary_objection"],
        discussed_price=turn["pricing_strategy"]["recommended_public_counter"],
        lead_status=turn["lead"]["status"],
        payment_summary=str(turn["payment_estimate"]),
        trade_in_summary=str(trade) if trade else "not discussed",
        risk_summary=str(turn["deal_integrity"]["risk_signals"]),
    )


__all__ = ["evaluate_negotiation_turn", "build_initial_negotiation_brief"]


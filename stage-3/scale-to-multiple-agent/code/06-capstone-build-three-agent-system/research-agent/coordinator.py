import asyncio
import json

import anthropic

from account_subagent import lookup_account
from policy_subagent import lookup_policies


def _extract_text(response: anthropic.types.Message) -> str:
    for block in response.content:
        if hasattr(block, "text"):
            return block.text
    return ""


async def run_account_subagent_async(customer_id: str) -> dict:
    """Async wrapper around the synchronous account lookup."""

    return await asyncio.to_thread(lookup_account, customer_id)


async def run_policy_subagent_async(flag_type: str) -> dict:
    """Async wrapper around the synchronous policy lookup."""

    return await asyncio.to_thread(lookup_policies, flag_type)


async def investigate_flagged_account(customer_id: str, flag_reason: str) -> str:
    """
    Coordinate the investigation of a flagged account.

    The account and policy lookups run in parallel using asyncio.gather().
    """

    client = anthropic.Anthropic()

    print(f"Starting parallel investigation for customer {customer_id}...")
    print("Running account lookup and policy lookup simultaneously...")

    account_result, policy_result = await asyncio.gather(
        run_account_subagent_async(customer_id),
        run_policy_subagent_async(flag_reason),
        return_exceptions=False,
    )

    print(f"Account lookup: {account_result['status']}")
    print(f"Policy lookup: {policy_result['status']}")

    account_ok = account_result.get("status") == "success"
    policy_ok = policy_result.get("status") == "success"

    if not account_ok and not policy_ok:
        return (
            "Investigation could not be completed. Both data sources are "
            "currently unavailable:\n\n"
            f"Account lookup: {account_result.get('message', 'Unknown error')}\n"
            f"Policy lookup: {policy_result.get('message', 'Unknown error')}\n\n"
            "Please try again in a few minutes or contact support directly."
        )

    synthesis_input = {
        "investigation_subject": {"customer_id": customer_id, "flag_reason": flag_reason},
        "account_data": account_result.get("data") if account_ok else None,
        "policy_data": policy_result.get("data") if policy_ok else None,
        "coverage_notes": [],
    }

    if not account_ok:
        synthesis_input["coverage_notes"].append(
            {
                "source": "account_lookup",
                "status": "failed",
                "error_type": account_result.get("error_type"),
                "message": account_result.get("message"),
                "retryable": account_result.get("retryable", False),
            }
        )

    if not policy_ok:
        synthesis_input["coverage_notes"].append(
            {
                "source": "policy_lookup",
                "status": "failed",
                "error_type": policy_result.get("error_type"),
                "message": policy_result.get("message"),
                "retryable": policy_result.get("retryable", False),
            }
        )

    print("Running synthesis...")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=(
            "You are a customer support synthesis agent. You receive structured "
            "research data from account and policy lookup agents and produce a "
            "clear, helpful response for the customer.\n\n"
            "Requirements:\n"
            "- Reference specific dates, flag types, and policy names from the data\n"
            "- Cite the policy URL when describing customer rights or options\n"
            "- If coverage_notes contains entries, explicitly acknowledge those "
            "gaps — state what data is unavailable and why it matters\n"
            "- Do not speculate about missing data or fill gaps with assumptions\n"
            "- Be specific and direct — the customer wants to understand their "
            "situation, not receive generic reassurance"
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    "A customer has asked about their flagged account. "
                    "Here is the research data:\n\n"
                    f"{json.dumps(synthesis_input, indent=2)}\n\n"
                    "Produce a response that explains: what the flag is and why it was "
                    "applied, what feature restrictions are active, what policies apply, "
                    "and what options the customer has going forward."
                ),
            }
        ],
    )

    return _extract_text(response)

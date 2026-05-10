import json

import anthropic

from mock_data import POLICIES


def lookup_policies(flag_type: str) -> dict:
    """
    Look up policies relevant to a specific flag type.

    Takes the flag_type from the account lookup result and returns
    the applicable policies with full source attribution.
    """

    client = anthropic.Anthropic()

    policy_tool = {
        "name": "get_policies",
        "description": (
            "Look up the policies that apply to a specific account flag type. "
            "Returns customer rights, appeal options, and removal conditions. "
            "Always cite the specific policy document URL in your response."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "flag_type": {
                    "type": "string",
                    "description": (
                        "The type of flag to look up policies for "
                        "(e.g. 'payment_dispute', 'fraud_suspicion')"
                    ),
                }
            },
            "required": ["flag_type"],
        },
    }

    messages = [
        {
            "role": "user",
            "content": (
                f"Find the policies that apply to a '{flag_type}' account flag. "
                f"Return the customer rights, appeal process, and conditions for "
                f"flag removal. Include the policy URL as a citation."
            ),
        }
    ]

    try:
        while True:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=(
                    "You are a policy research specialist. "
                    "Use the get_policies tool to look up applicable policies. "
                    "Always include the policy URL in your response. "
                    "Return only what the policy documents actually say — "
                    "do not interpret or expand on the written policies."
                ),
                tools=[policy_tool],
                messages=messages,
                timeout=15.0,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        try:
                            return {"status": "success", "data": json.loads(block.text)}
                        except json.JSONDecodeError:
                            return {
                                "status": "success",
                                "data": {"raw_response": block.text},
                            }
                return {"status": "success", "data": {}}

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = _execute_policy_tool(block.name, block.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": json.dumps(result),
                            }
                        )

                messages.append({"role": "user", "content": tool_results})

    except anthropic.APITimeoutError:
        return {
            "status": "failed",
            "error_type": "timeout",
            "retryable": True,
            "attempted": f"policy lookup for flag type: {flag_type}",
            "partial_data": None,
            "message": "Policy lookup timed out.",
        }
    except anthropic.APIStatusError as e:
        return {
            "status": "failed",
            "error_type": "api_error",
            "retryable": e.status_code == 429,
            "attempted": f"policy lookup for flag type: {flag_type}",
            "partial_data": None,
            "message": f"API error {e.status_code}: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "failed",
            "error_type": "unknown",
            "retryable": False,
            "attempted": f"policy lookup for flag type: {flag_type}",
            "partial_data": None,
            "message": str(e),
        }


def _execute_policy_tool(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "get_policies":
        flag_type = tool_input.get("flag_type", "")
        policy = POLICIES.get(flag_type)

        if policy:
            return policy

        return {
            "error": "policy_not_found",
            "message": f"No policy found for flag type: {flag_type}",
            "available_types": list(POLICIES.keys()),
        }

    return {
        "error": "unknown_tool",
        "message": f"Tool '{tool_name}' is not available to this agent.",
    }

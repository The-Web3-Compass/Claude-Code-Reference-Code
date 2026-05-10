import json

import anthropic

from mock_data import ACCOUNTS


def lookup_account(customer_id: str) -> dict:
    """
    Look up account details for a customer.

    Returns a structured result with status, data, and error information.
    The coordinator uses this structure to decide what to do next —
    whether to proceed, retry, or handle a failure gracefully.
    """

    client = anthropic.Anthropic()

    account_tool = {
        "name": "get_account_details",
        "description": (
            "Look up a customer's account record including flag status, "
            "feature restrictions, and account history. "
            "Use this to retrieve the current state of any customer account."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer ID to look up (e.g. 'CUST-4492')",
                }
            },
            "required": ["customer_id"],
        },
    }

    messages = [
        {
            "role": "user",
            "content": (
                f"Look up the account details for customer {customer_id}. "
                f"Return the full account record including any flags and "
                f"feature restrictions."
            ),
        }
    ]

    try:
        while True:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=(
                    "You are an account investigation specialist. "
                    "Use the get_account_details tool to look up customer accounts. "
                    "Return only what the account record contains — do not infer "
                    "or guess any values that are not explicitly in the record."
                ),
                tools=[account_tool],
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
                        result = _execute_account_tool(block.name, block.input)
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
            "attempted": f"account lookup for {customer_id}",
            "partial_data": None,
            "message": "Account lookup timed out. The service may be under load.",
        }
    except anthropic.APIStatusError as e:
        return {
            "status": "failed",
            "error_type": "api_error",
            "retryable": e.status_code == 429,
            "attempted": f"account lookup for {customer_id}",
            "partial_data": None,
            "message": f"API error {e.status_code}: {str(e)}",
        }
    except Exception as e:
        return {
            "status": "failed",
            "error_type": "unknown",
            "retryable": False,
            "attempted": f"account lookup for {customer_id}",
            "partial_data": None,
            "message": str(e),
        }


def _execute_account_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Execute a tool call from the account subagent against the mock data.
    In a real system this would be a database query or API call.
    """

    if tool_name == "get_account_details":
        customer_id = tool_input.get("customer_id", "")
        account = ACCOUNTS.get(customer_id)

        if account:
            return account

        return {
            "error": "account_not_found",
            "message": f"No account found for customer ID: {customer_id}",
        }

    return {
        "error": "unknown_tool",
        "message": f"Tool '{tool_name}' is not available to this agent.",
    }

import json

from mock_data import CUSTOMERS, ORDERS


def get_customer(query: str, session_state: dict) -> str:
    query = query.strip().lower()

    for customer in CUSTOMERS.values():
        if (
            query == customer["customer_id"].lower()
            or query == customer["email"].lower()
            or query == customer["name"].lower()
        ):
            session_state["verified_customer_id"] = customer["customer_id"]
            session_state["verified_customer_name"] = customer["name"]

            return json.dumps(customer)

    return json.dumps(
        {
            "error": {
                "type": "validation",
                "retryable": False,
                "message": (
                    f"No customer found matching '{query}'. The input may be "
                    "misspelled or in the wrong format. Customer IDs follow the "
                    "format CUST-XXXX. You can also search by full name or "
                    "email address. Ask the customer to verify their details."
                ),
            }
        }
    )


def lookup_order(order_id: str, session_state: dict) -> str:
    order_id = order_id.strip().upper()

    if order_id in ORDERS:
        return json.dumps(ORDERS[order_id])

    return json.dumps(
        {
            "error": {
                "type": "validation",
                "retryable": False,
                "message": (
                    f"No order found with ID '{order_id}'. The order ID may be "
                    "incorrect or in the wrong format. Order IDs follow the format "
                    "ORD-XXXX (e.g. 'ORD-8821'). Ask the customer to double-check the "
                    "order number from their confirmation email/receipt and try again."
                ),
            }
        }
    )


def process_refund(customer_id: str, order_id: str, amount: float, session_state: dict) -> str:
    if not session_state.get("verified_customer_id"):
        return json.dumps(
            {
                "error": {
                    "type": "permission",
                    "retryable": False,
                    "message": (
                        "Cannot process a refund before customer identity has been "
                        "verified. Call get_customer first and confirm the customer's "
                        "identity before attempting a refund."
                    ),
                }
            }
        )

    if customer_id != session_state["verified_customer_id"]:
        return json.dumps(
            {
                "error": {
                    "type": "permission",
                    "retryable": False,
                    "message": (
                        "Customer ID mismatch. The verified customer in this session is "
                        f"{session_state['verified_customer_id']} but the refund request "
                        f"is for {customer_id}. Do not process this refund. Verify you "
                        "have the correct customer before continuing."
                    ),
                }
            }
        )

    if order_id not in ORDERS:
        return json.dumps(
            {
                "error": {
                    "type": "validation",
                    "retryable": False,
                    "message": (
                        f"Order {order_id} not found. Verify the order ID with the "
                        "customer and try again."
                    ),
                }
            }
        )

    order = ORDERS[order_id]
    if order["customer_id"] != session_state["verified_customer_id"]:
        return json.dumps(
            {
                "error": {
                    "type": "permission",
                    "retryable": False,
                    "message": (
                        f"Order {order_id} does not belong to the verified customer. "
                        "Do not process this refund."
                    ),
                }
            }
        )

    return json.dumps(
        {
            "success": True,
            "refund_id": "REF-" + order_id.split("-")[1],
            "customer_id": customer_id,
            "order_id": order_id,
            "amount": amount,
            "status": "initiated",
            "message": (
                f"Refund of ${amount:.2f} for order {order_id} has been initiated. "
                "Funds will return to the original payment method within 3-5 business days."
            ),
        }
    )


def run_tool(tool_name: str, tool_input: dict, session_state: dict) -> str:
    if tool_name == "get_customer":
        return get_customer(tool_input["query"], session_state)
    if tool_name == "lookup_order":
        return lookup_order(tool_input["order_id"], session_state)
    if tool_name == "process_refund":
        return process_refund(
            tool_input["customer_id"],
            tool_input["order_id"],
            tool_input["amount"],
            session_state,
        )

    return json.dumps(
        {
            "error": {
                "type": "validation",
                "retryable": False,
                "message": f"Tool '{tool_name}' is not recognised.",
            }
        }
    )

import json

from mock_data import CUSTOMERS, ORDERS


def get_customer(query: str) -> str:
    query = query.strip().lower()

    for customer in CUSTOMERS.values():
        if (
            query == customer["customer_id"].lower()
            or query == customer["email"].lower()
            or query == customer["name"].lower()
        ):
            return json.dumps(customer)

    return json.dumps(
        {
            "error": {
                "type": "validation",
                "retryable": False,
                "message": (
                    f"No customer found matching '{query}'. The input may be "
                    "misspelled or in the wrong format. Customer IDs follow the "
                    "format CUST-XXXX. You can also search by full name or email "
                    "address. Ask the customer to verify their details and try again."
                ),
            }
        }
    )


def lookup_order(order_id: str) -> str:
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


def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "get_customer":
        return get_customer(tool_input["query"])
    if tool_name == "lookup_order":
        return lookup_order(tool_input["order_id"])

    return json.dumps(
        {
            "error": {
                "type": "validation",
                "retryable": False,
                "message": f"Tool '{tool_name}' is not recognised.",
            }
        }
    )

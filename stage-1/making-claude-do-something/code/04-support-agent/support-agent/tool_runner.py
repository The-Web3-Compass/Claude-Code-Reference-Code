# tool_runner.py

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
            "error": "customer_not_found",
            "message": f"No customer found matching '{query}'. "
            "Please check the name, email, or customer ID and try again.",
        }
    )


def lookup_order(order_id: str) -> str:
    order_id = order_id.strip().upper()

    if order_id in ORDERS:
        return json.dumps(ORDERS[order_id])

    return json.dumps(
        {
            "error": "order_not_found",
            "message": f"No order found with ID '{order_id}'. "
            "Please check the order ID and try again.",
        }
    )


def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "get_customer":
        return get_customer(tool_input["query"])
    elif tool_name == "lookup_order":
        return lookup_order(tool_input["order_id"])
    else:
        return json.dumps(
            {
                "error": "unknown_tool",
                "message": f"Tool '{tool_name}' is not recognised.",
            }
        )

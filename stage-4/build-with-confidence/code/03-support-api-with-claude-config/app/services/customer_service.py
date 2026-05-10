from app.errors import AppError
from app.models.customer import Customer


def get_customer(customer_id: str) -> Customer:
    if not customer_id:
        raise AppError("invalid_customer_id", "customer_id is required", status=400)

    if customer_id != "cust_123":
        raise AppError("customer_not_found", f"Customer {customer_id} not found", status=404)

    return Customer(id="cust_123", email="customer@example.com")

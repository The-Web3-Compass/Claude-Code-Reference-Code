ACCOUNTS = {
    "CUST-4492": {
        "customer_id": "CUST-4492",
        "name": "Sarah Chen",
        "email": "sarah.chen@email.com",
        "account_status": "restricted",
        "flag_type": "payment_dispute",
        "flag_applied_at": "2024-01-10T09:15:00Z",
        "flag_trigger": "Chargeback filed on order ORD-8821",
        "feature_restrictions": [
            {
                "feature": "international_payments",
                "restricted_at": "2024-01-10T09:15:00Z",
                "reason": "Automatic restriction on payment_dispute flag",
            },
            {
                "feature": "instant_transfers",
                "restricted_at": "2024-01-10T09:15:00Z",
                "reason": "Automatic restriction on payment_dispute flag",
            },
        ],
        "previous_flags": [],
    },
    "CUST-2201": {
        "customer_id": "CUST-2201",
        "name": "James Okafor",
        "email": "james.okafor@email.com",
        "account_status": "active",
        "flag_type": None,
        "flag_applied_at": None,
        "flag_trigger": None,
        "feature_restrictions": [],
        "previous_flags": [],
    },
}

POLICIES = {
    "payment_dispute": {
        "policy_name": "Payment Dispute and Chargeback Policy",
        "policy_url": "https://policies.example.com/payment-dispute",
        "version": "2.1",
        "last_updated": "2023-09-01",
        "customer_rights": (
            "Customers have the right to know why their account was flagged "
            "within 48 hours of the flag being applied. Customers may request "
            "a full account review at any time."
        ),
        "appeal_process": (
            "Submit an appeal through the Account Review portal or by contacting "
            "support directly. Appeals are reviewed within 5 business days."
        ),
        "removal_conditions": (
            "The flag is removed when: (1) the chargeback dispute is resolved in "
            "the customer's favour, (2) the customer provides documentation that "
            "the dispute was filed in error, or (3) 180 days pass with no further "
            "payment disputes."
        ),
        "feature_restoration": (
            "Restricted features are restored within 24 hours of the flag being removed."
        ),
    },
    "fraud_suspicion": {
        "policy_name": "Fraud Suspicion and Account Protection Policy",
        "policy_url": "https://policies.example.com/fraud-suspicion",
        "version": "3.0",
        "last_updated": "2024-01-01",
        "customer_rights": (
            "Customers have the right to request a full explanation of the "
            "suspicious activity that triggered the flag. Identity verification "
            "may be required before account restrictions are lifted."
        ),
        "appeal_process": (
            "Contact the fraud review team directly. Standard review takes "
            "3-7 business days. Expedited review is available for account holders "
            "with no prior flags."
        ),
        "removal_conditions": (
            "The flag is removed after successful identity verification and "
            "confirmation that the flagged activity was legitimate."
        ),
        "feature_restoration": (
            "Features are restored progressively over 7 days following flag removal "
            "to monitor for anomalous activity."
        ),
    },
}

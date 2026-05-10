import asyncio

from dotenv import load_dotenv

from coordinator import investigate_flagged_account

load_dotenv()


async def main():
    print("\n" + "=" * 50)
    print("Three-Agent Research System")
    print("=" * 50 + "\n")

    print("TEST CASE 1: Happy path")
    print("-" * 30)
    result = await investigate_flagged_account(
        customer_id="CUST-4492",
        flag_reason="payment_dispute",
    )
    print("\nFinal response:")
    print(result)

    print("\n" + "=" * 50 + "\n")

    print("TEST CASE 2: No flag on account")
    print("-" * 30)
    result = await investigate_flagged_account(
        customer_id="CUST-2201",
        flag_reason="payment_dispute",
    )
    print("\nFinal response:")
    print(result)

    print("\n" + "=" * 50 + "\n")

    print("TEST CASE 3: Unknown customer")
    print("-" * 30)
    result = await investigate_flagged_account(
        customer_id="CUST-9999",
        flag_reason="payment_dispute",
    )
    print("\nFinal response:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

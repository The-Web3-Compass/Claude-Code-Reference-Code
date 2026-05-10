from anthropic import Anthropic
from dotenv import load_dotenv

from tool_runner import run_tool
from tools import tools

load_dotenv()

client = Anthropic()

SYSTEM_PROMPT = """You are a customer support agent for an online retailer.
You have access to tools that let you look up customer records and order details.

When a customer contacts you:
1. Look up their account using get_customer before doing anything else.
2. Use lookup_order to get details on any specific order they mention.
3. Give clear, helpful responses based on what you find.
4. If you cannot find a customer or order, tell them politely and ask them
   to double-check the information they provided.

Always verify who you are speaking with before discussing account details."""


def run_agent(user_message: str) -> str:
    conversation_history = [{"role": "user", "content": user_message}]

    session_state = {
        "verified_customer_id": None,
        "verified_customer_name": None,
    }

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=conversation_history,
        )

        conversation_history.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = run_tool(block.name, block.input, session_state)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            conversation_history.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("Customer Support Agent, Stage 1")
    print("Type 'quit' to exit")
    print("=" * 40)

    while True:
        user_input = input("\nCustomer: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nAgent:", end=" ", flush=True)
        response = run_agent(user_input)
        print(response)

> *This log shows a complete interaction between a customer and the support agent.*
> *Read it top to bottom. Every field is real, this is exactly what the API* returns.

---

## TURN 1 — Customer message comes in

```
role: user

content:
  - type: text
    text: |
      Hi, my name is Sarah Chen and my order number is ORD-8821. I placed it
      six days ago and it still hasn't shipped. Can you help me figure out
      what's going on?
```

---

## TURN 2 — Claude's first response

```
role: assistant
stop_reason: tool_use

content:
  - type: text
    text: |
      Let me pull up your account and order details so I can see
      what's happening.

  - type: tool_use
    id: call_01
    name: get_customer
    input:
      query: "Sarah Chen"
```

> **What just happened:** Claude responded with stop_reason: tool_use. It needs customer account data before it can help, so it called get_customer with the name from the customer's message. Your code needs to run that tool and send the result back before calling the API again. Notice that this assistant message contains both a text block and a tool_use block, both are part of the same response.

---

## TURN 3 — Tool result sent back to Claude

```
role: user

content:
  - type: tool_result
    tool_use_id: call_01
    content:
      - type: text
        text: |
          {
            "customer_id": "CUST-4492",
            "name": "Sarah Chen",
            "email": "sarah.chen@email.com",
            "account_status": "active",
            "member_since": "2021-03-14",
            "total_orders": 12,
            "orders": [
              "ORD-8821",
              "ORD-7103",
              "ORD-6897"
            ]
          }
```

> **What Claude has now:** a verified customer record. It knows the account is active, it can see the order history, and it can confirm that ORD-8821 is on this customer's account. The tool_use_id: call_01 ties this result back to the tool call that requested it. Tool results always go back in as user role messages.
> 

---

## TURN 4 — Claude's second response

```
role: assistant
stop_reason: tool_use

content:
  - type: tool_use
    id: call_02
    name: lookup_order
    input:
      order_id: "ORD-8821"
```

> **What just happened:** stop_reason: tool_use again. Claude verified the customer but still doesn't know anything about the specific order, just that it exists. So it called lookup_order with the order ID the customer provided in their original message. Note that Claude went straight to the tool call this time with no text block first. Your code runs lookup_order and sends the result back.

---

## TURN 5 — Second tool result sent back to Claude

```
role: user

content:
  - type: tool_result
    tool_use_id: call_02
    content:
      - type: text
        text: |
          {
            "order_id": "ORD-8821",
            "customer_id": "CUST-4492",
            "status": "processing",
            "items": [
              {
                "product": "Wireless Keyboard",
                "quantity": 1,
                "price": 79.99
              }
            ],
            "placed_at": "2024-01-08T14:23:00Z",
            "estimated_ship_date": "2024-01-12T00:00:00Z",
            "actual_ship_date": null,
            "carrier": null,
            "tracking_number": null,
            "notes": "Item held for warehouse inventory check. Expected to resolve within 24-48 hours."
          }
```

> **What Claude has now:** the full order record. The order is in processing, the estimated ship date has passed, nothing has shipped, and there's a note explaining why, a warehouse inventory hold expected to resolve in 24 to 48 hours. Claude now has everything it needs to give the customer a real answer.

---

## TURN 6 — Claude's final response

```
role: assistant
stop_reason: end_turn

content:
  - type: text
    text: |
      Hi Sarah, I've pulled up your account and your order. Here's what's
      happening with ORD-8821.

      Your order for the Wireless Keyboard is currently in processing and has
      been held for a warehouse inventory check. That's what's caused the delay
      past your original estimated ship date of January 12th. According to the
      notes on the order, the hold is expected to resolve within 24 to 48 hours,
      after which your order should ship.

      There's nothing you need to do on your end — the warehouse team is actively
      working through it. Once it ships you'll receive a confirmation email with
      tracking information.

      If it hasn't moved by tomorrow afternoon, feel free to come back and I'll
      escalate it for you.
```

> **What just happened:** stop_reason: end_turn. The loop is done. Claude used data from both tool results to produce a specific, accurate response, the reason for the delay, the resolution timeline, what happens next, and an offer to escalate. Your code surfaces this response to the user and stops looping.
> 

---

## Full Loop Summary

```
Step 1   User message arrives
         ↓
Step 2   Claude responds — stop_reason: tool_use
         → Your code calls get_customer("Sarah Chen")
         ↓
Step 3   Tool result sent back as user message (tool_use_id: call_01)
         ↓
Step 4   Claude responds — stop_reason: tool_use
         → Your code calls lookup_order("ORD-8821")
         ↓
Step 5   Tool result sent back as user message (tool_use_id: call_02)
         ↓
Step 6   Claude responds — stop_reason: end_turn
         → Surface response to user, stop loop
```

**Total loop iterations:** 2
**Tools called:** get_customer, lookup_order
**Final outcome:** Customer informed of delay reason and expected resolution timeline.
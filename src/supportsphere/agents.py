"""Coordinator and focused specialist workflows."""
import re
from . import tools
from .policy import ToolRegistry
from .memory import ConversationMemory

BILLING, SHIPPING, REFUNDS = "billing", "shipping", "refunds"

def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("lookup_invoice", tools.lookup_invoice)
    registry.register("get_order_status", tools.get_order_status)
    registry.register("get_refund_policy", tools.get_refund_policy)
    registry.grant(BILLING, "lookup_invoice")
    registry.grant(SHIPPING, "get_order_status")
    registry.grant(REFUNDS, "get_refund_policy")
    return registry

class SupportCoordinator:
    def __init__(self, memory: ConversationMemory | None = None):
        self.registry = build_registry()
        self.memory = memory or ConversationMemory()

    @staticmethod
    def route(message: str) -> str:
        text = message.lower()
        if re.search(r"\b(invoice|billing|payment|charged|charge)\b", text):
            return BILLING
        if re.search(r"\b(order|shipping|shipment|delivery|tracking|track)\b", text):
            return SHIPPING
        if re.search(r"\b(refund|return|money back)\b", text):
            return REFUNDS
        return "general"

    def handle(self, message: str, session_id: str = "default") -> dict:
        specialist = self.route(message)
        if specialist == BILLING:
            match = re.search(r"\bINV-\d+\b", message, re.I)
            result = self.registry.call(BILLING, "lookup_invoice", invoice_id=match.group(0)) if match else {"error": "Please share your invoice ID (for example, INV-1042)."}
            answer = self._billing_reply(result)
        elif specialist == SHIPPING:
            match = re.search(r"\bORD-\d+\b", message, re.I)
            result = self.registry.call(SHIPPING, "get_order_status", order_id=match.group(0)) if match else {"error": "Please share your order ID (for example, ORD-8871)."}
            answer = self._shipping_reply(result)
        elif specialist == REFUNDS:
            result = self.registry.call(REFUNDS, "get_refund_policy")
            answer = (f"Our demo policy allows refunds within {result['window_days']} days for "
                      f"{result['condition'].lower()}. Processing usually takes {result['processing_days']}.")
        else:
            result = {"route": "general"}
            answer = "I can help with invoices, order tracking, and refund-policy questions. Which one would you like help with?"
        self.memory.add_turn(session_id, message, answer)
        return {"route": specialist, "tool_result": result, "answer": answer}

    @staticmethod
    def _billing_reply(data: dict) -> str:
        if data.get("error"):
            return data["error"] + " Please verify the ID and try again."
        return f"Invoice {data['invoice_id']} is {data['status']} for {data['currency']} {data['amount']:.2f}. Due date: {data['due_date']}."

    @staticmethod
    def _shipping_reply(data: dict) -> str:
        if data.get("error"):
            return data["error"] + " Please verify the ID and try again."
        return f"Order {data['order_id']} is {data['status']} with {data['carrier']}. Estimated delivery: {data['eta']}."

"""Fixture-backed customer support tools. Replace with authenticated API adapters."""
INVOICES = {
    "INV-1042": {"status": "paid", "amount": 129.99, "currency": "USD", "due_date": "2026-10-15"},
    "INV-2048": {"status": "overdue", "amount": 89.50, "currency": "USD", "due_date": "2026-10-28"},
}
ORDERS = {
    "ORD-8871": {"status": "in transit", "carrier": "ParcelPost", "eta": "2026-11-09"},
    "ORD-1200": {"status": "delivered", "carrier": "ParcelPost", "eta": "2026-11-03"},
}

def lookup_invoice(invoice_id: str) -> dict:
    """Look up a fictional invoice record."""
    record = INVOICES.get(invoice_id.upper())
    return {"invoice_id": invoice_id.upper(), **record} if record else {"error": "Invoice not found"}

def get_order_status(order_id: str) -> dict:
    """Look up a fictional order tracking record."""
    record = ORDERS.get(order_id.upper())
    return {"order_id": order_id.upper(), **record} if record else {"error": "Order not found"}

def get_refund_policy() -> dict:
    """Return the demo refund policy."""
    return {"window_days": 30, "condition": "Unused items in original condition", "processing_days": "5-7 business days"}

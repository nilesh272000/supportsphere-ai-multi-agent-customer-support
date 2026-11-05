import unittest
from supportsphere.agents import build_registry
from supportsphere.policy import ToolAccessDenied

class ToolPolicyTests(unittest.TestCase):
    def setUp(self):
        self.registry = build_registry()

    def test_shipping_cannot_access_invoice_tool(self):
        with self.assertRaises(ToolAccessDenied):
            self.registry.call("shipping", "lookup_invoice", invoice_id="INV-1042")

    def test_billing_can_access_invoice_tool(self):
        result = self.registry.call("billing", "lookup_invoice", invoice_id="INV-1042")
        self.assertEqual(result["status"], "paid")

    def test_unknown_specialist_has_no_permissions(self):
        with self.assertRaises(ToolAccessDenied):
            self.registry.call("unknown", "get_order_status", order_id="ORD-8871")

if __name__ == "__main__":
    unittest.main()

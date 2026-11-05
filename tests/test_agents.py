import tempfile
import unittest
from pathlib import Path
from supportsphere.agents import SupportCoordinator
from supportsphere.memory import ConversationMemory

class AgentWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.agent = SupportCoordinator(ConversationMemory(Path(self.temp.name) / "memory.json"))

    def tearDown(self):
        self.temp.cleanup()

    def test_shipping_route(self):
        result = self.agent.handle("Where is my order ORD-8871?")
        self.assertEqual(result["route"], "shipping")
        self.assertIn("in transit", result["answer"])

    def test_billing_route(self):
        result = self.agent.handle("Check invoice INV-1042")
        self.assertEqual(result["route"], "billing")
        self.assertIn("paid", result["answer"])

    def test_refund_route(self):
        result = self.agent.handle("What is your refund policy?")
        self.assertEqual(result["route"], "refunds")
        self.assertIn("30 days", result["answer"])

    def test_memory_persists_turn(self):
        self.agent.handle("Hello", session_id="s-1")
        self.assertEqual(len(self.agent.memory.recent("s-1")), 1)

if __name__ == "__main__":
    unittest.main()

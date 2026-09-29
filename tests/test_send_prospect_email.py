import os
import unittest
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTests(unittest.TestCase):
    def setUp(self):
        self.runtime = SimpleNamespace(config={"metadata": {}})

    def test_disqualified_prospects_are_blocked_without_message_id(self):
        for prospect_id in [f"LEAD-{number:05d}" for number in range(50001, 50006)]:
            with self.subTest(prospect_id=prospect_id):
                result = send_prospect_email.func(
                    {"prospect_id": prospect_id, "name": "Prospect", "email": "prospect@example.com"},
                    "Follow up",
                    "Hello",
                    self.runtime,
                )

                self.assertEqual(result["status"], "blocked")
                self.assertEqual(result["reason"], "prospect_disqualified")
                self.assertEqual(result["prospect_id"], prospect_id)
                self.assertNotIn("message_id", result)

    def test_eligible_prospect_is_sent(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-18993", "name": "Prospect", "email": "prospect@example.com"},
            "Follow up",
            "Hello",
            self.runtime,
        )

        self.assertEqual(result["status"], "sent")
        self.assertIn("message_id", result)


if __name__ == "__main__":
    unittest.main()

import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTest(unittest.TestCase):
    def test_update_persists_and_invalidates_cached_profile(self):
        prospect_id = "LEAD-12853"
        technology = "Test Technology"
        record = data_service.PROSPECTS[prospect_id]
        original_tech_stack = list(record["tech_stack"])
        original_profile = data_service._PROFILES.pop(prospect_id, None)

        try:
            profile = build_prospect_profile.invoke({"prospect_id": prospect_id})
            self.assertNotIn(technology, profile["prospect_profile"]["tech_stack"])

            result = data_service.update_prospect_info(prospect_id, technology)

            self.assertTrue(result["updated"])
            self.assertIn(technology, data_service.fetch_tech_stack(prospect_id))
            refreshed_profile = build_prospect_profile.invoke({"prospect_id": prospect_id})
            self.assertIn(technology, refreshed_profile["prospect_profile"]["tech_stack"])
        finally:
            record["tech_stack"] = original_tech_stack
            data_service._PROFILES.pop(prospect_id, None)
            if original_profile is not None:
                data_service._PROFILES[prospect_id] = original_profile

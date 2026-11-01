import os
import sys
import unittest

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine import reasoning


class TestTerraformScenarios(unittest.TestCase):

    def test_knowledge_base_loading(self):
        """Verify that kb/knowledge_base.json exists, is valid JSON, and loads all 9 stages."""
        kb = reasoning.load_knowledge_base()
        self.assertIn("stages", kb, "Knowledge base missing 'stages' root key.")
        stages = kb["stages"]
        self.assertGreaterEqual(len(stages), 9, f"Expected 9 stages in KB, found {len(stages)}")
        self.assertIn("stage_1_input_echo", stages)
        self.assertIn("stage_4_readiness_gate", stages)
        self.assertIn("stage_5_crop_suggestions", stages)

    def test_scenario_a_hardpan_slope_late_rains(self):
        """
        Scenario A: Continuous hardpan, fast runoff on slope, late rains.
        Verifies that the reasoning engine recommends hardpan fracturing, contour trenching,
        and weather/runoff-resilient crops (Finger Millet & Sorghum).
        """
        inputs = {
            "description": "Sloping land with hard subsurface crust and late rains.",
            "subsurface_layer": "Continuous hardpan / rock",
            "water_behavior": "Fast runoff",
            "local_advice": "No local advice available",
            "weather": "Late rains / unexpected dry spell"
        }

        # Stage 2: Missing Analysis
        res_st2 = reasoning.evaluate_stage_data("stage_2", inputs)
        self.assertIn("inferences", res_st2)
        self.assertTrue(any("rock/hardpan" in inf for inf in res_st2["inferences"]))

        # Stage 3: Fix Protocol
        res_st3 = reasoning.evaluate_stage_data("stage_3", inputs)
        actions_text = " ".join(res_st3.get("actions", []))
        self.assertTrue("hardpan" in actions_text.lower() or "grid points" in actions_text.lower())
        self.assertTrue("contour trenches" in actions_text.lower() or "runoff" in actions_text.lower())

        # Stage 5: Crop Suggestions
        res_st5 = reasoning.evaluate_stage_data("stage_5", inputs)
        crops = res_st5.get("crops", [])
        crop_names = [c["crop"] for c in crops]
        self.assertTrue(any("Millet" in c for c in crop_names))
        self.assertTrue(any("Sorghum" in c for c in crop_names))

    def test_scenario_b_flat_loose_gravel_pooling(self):
        """
        Scenario B: Loose gravel on flat land with water pooling.
        Verifies that the engine adapts recommendations to gravel soil management,
        raised drainage ridges, and tuber crops (Sweet Potato).
        """
        inputs = {
            "description": "Flat land where water pools during downpours.",
            "subsurface_layer": "Loose gravel",
            "water_behavior": "Pooling",
            "local_advice": "Reliable local advice available",
            "weather": "Normal seasonal"
        }

        # Stage 3: Fix Protocol
        res_st3 = reasoning.evaluate_stage_data("stage_3", inputs)
        actions_text = " ".join(res_st3.get("actions", []))
        self.assertTrue("gravel" in actions_text.lower() or "raised" in actions_text.lower() or "mounds" in actions_text.lower())

        # Stage 5: Crop Suggestions
        res_st5 = reasoning.evaluate_stage_data("stage_5", inputs)
        crops = res_st5.get("crops", [])
        sweet_potato_entry = next((c for c in crops if "Sweet Potato" in c["crop"]), None)
        self.assertIsNotNone(sweet_potato_entry, "Sweet Potato should be recommended for pooling terrain.")
        self.assertTrue(
            "DRAINAGE" in sweet_potato_entry["suitability"] or "WATERLOGGING" in sweet_potato_entry["suitability"] or "CONTROL" in sweet_potato_entry["suitability"]
        )

    def test_readiness_gate_enforcement(self):
        """
        Scenario C: Readiness Gate Enforcement.
        Verifies that unknown or failed physical checks yield a 'failed' status,
        and only explicitly passing checks result in a 'passed' gate status.
        """
        inputs = {
            "subsurface_layer": "Continuous hardpan / rock",
            "water_behavior": "Fast runoff"
        }

        # Case 1: Unverified / False checks -> Must fail
        failed_gate = reasoning.evaluate_readiness_gate(inputs, tool_penetrated=False, water_retained=False)
        self.assertEqual(failed_gate["status"], "failed")
        self.assertIn("Readiness check failed", failed_gate["explanation"])

        # Case 2: Partial check (Tool penetrated but water not retained) -> Must fail
        partial_gate = reasoning.evaluate_readiness_gate(inputs, tool_penetrated=True, water_retained=False)
        self.assertEqual(partial_gate["status"], "failed")

        # Case 3: Both observable checks verified -> Must pass
        passed_gate = reasoning.evaluate_readiness_gate(inputs, tool_penetrated=True, water_retained=True)
        self.assertEqual(passed_gate["status"], "passed")
        self.assertIn("Readiness gate cleared", passed_gate["explanation"])


if __name__ == "__main__":
    unittest.main()
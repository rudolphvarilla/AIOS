"""Unit tests for the controlled AIOS local-agent regression runner."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import agent  # noqa: E402


class RegressionReportTests(unittest.TestCase):
    def test_standard_cases_are_run_and_captured(self) -> None:
        result = {
            "ok": True,
            "command": ["python", "coordinator.py"],
            "cwd": "C:\\AIOS\\Coordinator",
            "returncode": 0,
            "stdout": "answer",
            "stderr": "",
            "elapsed_seconds": 1.25,
        }
        with patch.object(agent, "query_aios", return_value=result) as query_aios:
            report = agent.run_regression(Path("C:/AIOS/Coordinator"), timeout=17)

        self.assertTrue(report["ok"])
        self.assertEqual(report["report_type"], "aios_standard_regression")
        self.assertEqual(report["query_timeout_seconds"], 17)
        self.assertEqual([case["id"] for case in report["cases"]], ["R1", "R2", "R3"])
        self.assertEqual([case["status"] for case in report["cases"]], ["passed"] * 3)
        self.assertEqual(query_aios.call_count, 3)
        self.assertEqual(query_aios.call_args_list[0].args[1], "current weather in philippines")
        self.assertEqual(query_aios.call_args_list[1].args[1], "tallest mountain in the philippines")
        self.assertEqual(query_aios.call_args_list[2].args[1], "what is 2+2")
        self.assertTrue(all(call.kwargs["timeout"] == 17 for call in query_aios.call_args_list))

    def test_timeout_is_reported_without_hiding_output(self) -> None:
        timeout_result = {
            "ok": False,
            "command": ["python", "coordinator.py"],
            "cwd": "C:\\AIOS\\Coordinator",
            "returncode": None,
            "stdout": "partial output",
            "stderr": "partial error",
            "error": "timeout",
            "elapsed_seconds": 17.0,
        }
        with patch.object(agent, "query_aios", return_value=timeout_result):
            report = agent.run_regression(Path("C:/AIOS/Coordinator"), timeout=17)

        self.assertFalse(report["ok"])
        self.assertEqual([case["status"] for case in report["cases"]], ["timeout"] * 3)
        self.assertEqual(report["cases"][0]["stdout"], "partial output")
        self.assertEqual(report["cases"][0]["stderr"], "partial error")
        self.assertIsNone(report["cases"][0]["returncode"])

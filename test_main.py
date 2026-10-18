import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

import requests
from starlette.requests import Request


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "fiber_app", Path(__file__).with_name("main.py")
        )
        cls.main = importlib.util.module_from_spec(spec)
        # Importing the app must work even when all data services are offline.
        with patch("requests.get", side_effect=AssertionError("Startup fetched data")) as get:
            spec.loader.exec_module(cls.main)
            get.assert_not_called()

    def test_home_renders_without_data_services(self):
        request = Request({"type": "http", "method": "GET", "path": "/", "headers": []})
        with patch("requests.get", side_effect=requests.ConnectionError("Offline")):
            response = self.main.home(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Global Fiber Route Planner", response.body)

    def test_upstream_503_is_reported_before_decoding_html(self):
        for failed_request in range(3):
            with self.subTest(failed_request=failed_request):
                responses = [Mock() for _ in range(3)]
                for response in responses:
                    response.json.return_value = {"features": []}
                failed = responses[failed_request]
                failed.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
                with patch("requests.get", side_effect=responses) as get:
                    result = self.main.calculate_fiber(0, 0, 0, 1)
                self.assertEqual(result["status"], "error")
                self.assertIn("503", result["message"])
                failed.json.assert_not_called()
                for call in get.call_args_list:
                    self.assertEqual(call.kwargs["timeout"], 40)

    def test_upstream_timeout_is_reported(self):
        with patch("requests.get", side_effect=requests.Timeout("Data service timed out")):
            result = self.main.calculate_fiber(0, 0, 0, 1)
        self.assertEqual(result, {"status": "error", "message": "Data service timed out"})

    def test_route_calculation_with_available_data(self):
        terrestrial = {
            "features": [{
                "properties": {"operator_l": "Test Network"},
                "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 0]]},
            }]
        }
        responses = [Mock(), Mock(), Mock()]
        for response, data in zip(responses, [terrestrial, {"features": []}, {"features": []}]):
            response.json.return_value = data
        with patch("requests.get", side_effect=responses):
            result = self.main.calculate_fiber(0, 0, 0, 1)
        self.assertEqual(result["status"], "success")
        self.assertAlmostEqual(result["summary"]["total_km"], 111.19, places=2)
        self.assertEqual(result["partners"], ["Test Network"])
        self.assertEqual(result["segments"][0]["coords"], [[0, 0], [0, 1]])


if __name__ == "__main__":
    unittest.main()

import unittest

from unittest.mock import MagicMock, patch, Mock
import requests

from weather_service import get_forecast

class TestForecast(unittest.TestCase):
    @patch("weather_service.requests.get")
    def test_get_forecast_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [
                {"day": 1, "temp": {"day": 20}},
                {"day": 2, "temp": {"day": 22}},
            ]
        }
        mock_get.return_value = mock_response

        result = get_forecast("Paris", days=2)
        assert result == [
            {"day": 1, "temp": {"day": 20}},
            {"day": 2, "temp": {"day": 22}},
        ]
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["q"] == "Paris"
        assert kwargs["params"]["cnt"] == 2

    @patch("weather_service.requests.get")
    def test_get_forecast_non_200_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_forecast("UnknownCity")
        assert result is None

    @patch("weather_service.requests.get")
    def test_get_forecast_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = get_forecast("Paris")
        assert result is None
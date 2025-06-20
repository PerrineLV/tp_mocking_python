import unittest
from unittest.mock import Mock, patch
import requests
from weather_service import get_temperature

class TestWeather(unittest.TestCase):

    def setUp(self):
        """Fixture : prépare les données avant chaque test"""
        # Créez self.sample_weather_data avec des données météo types
        self.sample_weather_data = {
            'main': {
                'temp': 20.5,
                'pressure': 1012,
                'humidity': 60
            },
            'weather': [{
                'description': 'clear sky'
            }]
        }
        # Créez self.test_city avec une ville de test
        self.test_city = "Paris"

    @patch('weather_service.requests.get')
    def test_get_temperature_success(self, mock_get):
        """Test avec données de la fixture"""
        fake_response = Mock()
        fake_response.status_code = 200
        # Utilisez self.sample_weather_data ici
        fake_response.json.return_value = self.sample_weather_data

        mock_get.return_value = fake_response

        # Utilisez self.test_city
        result = get_temperature(self.test_city)

        # Complétez les assertions
        self.assertEqual(result, self.sample_weather_data['main']['temp'])
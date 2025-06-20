import unittest
from unittest.mock import Mock, mock_open, patch
import requests
from weather_service import get_temperature, save_weather_report

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

    class TestWeatherReport(unittest.TestCase):

        def setUp(self):
            """Fixture : prépare les données avant chaque test"""
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
            self.test_city = "Paris"
            self.filename = "test_weather_log.json"
        
        @patch('weather_service.datetime')
        @patch('builtins.open', new_callable=mock_open, read_data='[]')
        @patch('weather_service.get_temperature')
        def test_save_weather_report_success(self, mock_get_temp, mock_file,
            mock_datetime):
            """Test sauvegarde rapport météo - EXERCICE PRINCIPAL"""

            # Configurez mock_get_temp pour retourner 20.5
            mock_get_temp.return_value = 20.5

            # Configurez mock_datetime.now().isoformat() pour retourner une date fixe
            mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T12:00:00"

            # Appelez save_weather_report("Paris")
            result = save_weather_report("Paris")

            # Vérifiez que le résultat est True
            self.assertTrue(result)

            # Vérifiez que get_temperature a été appelé avec "Paris"
            mock_get_temp.assert_called_with("Paris")

            # Vérifiez que le fichier a été ouvert en lecture puis en écriture
            mock_file.assert_called_with(self.filename, "w")

            pass

        @patch('weather_service.requests.get')
        def test_multiple_cities(self, mock_get):
            """Test plusieurs villes avec une seule méthode"""

            cities_and_temps = [
                ("Paris", 25.0),
                ("Londres", 18.5),
                ("Tokyo", 30.2)
            ]

            for city, expected_temp in cities_and_temps:
                with self.subTest(city=city):
                    # Configurez le mock pour cette ville
                    mock_get.return_value = Mock(status_code=200, json=lambda: {
                        'main': {'temp': expected_temp}
                    })

                    # Testez get_temperature(city)
                    result = get_temperature(city)

                    # Vérifiez le résultat
                    self.assertEqual(result, expected_temp)
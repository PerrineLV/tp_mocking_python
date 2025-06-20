import unittest
from unittest.mock import Mock, patch
from weather_service import get_temperature
class TestWeather(unittest.TestCase):

    @patch('weather_service.requests.get')
    def test_get_temperature_paris(self, mock_get):
        """Premierest avec mock"""

        # 1. CRÉEZ un objet Mock pour simuler la réponse HTTP
        fake_response = Mock()
        fake_response.status_code = 200

        # 2. CRÉEZ les données JSON que l'API retournerait
        fake_response.json.return_value = {
            'main': {
                'temp': 25.5
            }
        }

        # 3. CONFIGUREZ le mock pour retourner votre fake_response
        mock_get.return_value = fake_response

        # 4. TESTEZ votre fonction
        result = get_temperature('Paris')

        # 5. VERIFIEZ le résultat
        self.assertEqual(result, 25.5)

        # 6. VÉRIFIEZ que requests.get a été appelé correctement
        mock_get.assert_called_once_with('http://api.openweathermap.org/data/2.5/weather',
                                           params={'q': 'Paris', 'appid': 'fake_api_key', 'units': 'metric'})

    @patch('weather_service.requests.get')
    def test_get_temperature_city_not_found(self, mock_get):
        """Test quand la ville n'existe pas"""

        # Créez un Mock qui retourne status_code = 404
        mock_response = Mock()
        mock_response.status_code = 404

        # Configurez mock_get.return_value
        mock_get.return_value = mock_response

        # Testez get_temperature("VilleInexistante")
        result = get_temperature("VilleInexistante")

        # Vérifiez que le résultat est None
        self.assertIsNone(result)

    if __name__ == '__main__':
        unittest.main()
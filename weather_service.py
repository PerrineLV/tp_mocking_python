import requests
def get_temperature(city):
    """Récupère la température d'une ville via une API"""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': '441f54eb9b8819b3a05d1674294bb055',
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        print(response.status_code)  # Pour déboguer, à supprimer en prod

        if response.status_code == 200:
            data = response.json()
            return data['main']['temp']
        else:
            return None
    except requests.exceptions.RequestException:
        return None
import requests
import json
from datetime import datetime

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

        if response.status_code == 200:
            data = response.json()
            return data['main']['temp']
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def save_weather_report(city, filename="weather_log.json"):
    """Récupère la météo et la sauvegarde dans un fichier"""

    # 1. Récupérer la température
    temp = get_temperature(city)
    if temp is None:
        return False

    # 2. Créer le rapport
    report = {
        'city': city,
        'temperature': temp,
        'timestamp': datetime.now().isoformat()
    }

    # 3. Sauvegarder dans le fichier
    try:
    # Lire le fichier existant
        with open(filename, 'r') as f:
            reports = json.load(f)
    except FileNotFoundError:
        reports = []

    reports.append(report)

    with open(filename, 'w') as f:
        json.dump(reports, f)

    return True

def get_forecast(city, days=5):
    """Récupère la prévision météo pour plusieurs jours"""
    url = f"http://api.openweathermap.org/data/2.5/forecast/daily"
    params = {
        'q': city,
        'cnt': days,
        'appid': '441f54eb9b8819b3a05d1674294bb055',
        'units': 'metric'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['list']
        else:
            return None
    except requests.exceptions.RequestException:
        return None
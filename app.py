import os
import threading
import time
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Definicja konfiguracji w słowniku
config = {
    "sections": [
        {
            "name": "Apple",
            "icon": "apple.svg",
            "links": [
                {
                    "name": "ApplePay",
                    "href": "https://www.apple.com/pl/apple-pay/",
                    "icon": "applepay.svg",
                },
            ],
        },
        {
            "name": "My services",
            "icon": "social.png",
            "links": [
                {
                    "name": "Second Home Page",
                    "href": "http://192.168.0.31:5001",
                    "icon": "facebook.svg",
                    "health-check": "http://192.168.0.31:5001/live"
                },
                {
                    "name": "Pihole",
                    "href": "http://192.168.0.31/admin",
                    "icon": "pihole.svg",
                    "health-check": "http://192.168.0.31/admin/api.php?status&auth=756bc47cb5215dc3329ca7e1f7be33a2dad68990bb94b76d90aa07f4e44a233a"
                },
            ],
        },
    ],
    "search": {
        "placeholder": "Search the web...",
        "name": "Google",
        "url": "https://www.google.com/search",
    },
    "fallbackIcon": {"name": "deutschebank.svg"},
}

# Liveness check: check if the application is alive
@app.route('/live')
def liveness():
    response = {
        "status": "alive",
        "message": "The application is running!"
    }
    return jsonify(response), 200

def check_health_status():
    for section in config['sections']:
        for link in section.get('links', []):
            health_check_url = link.get('health-check')
            if health_check_url:
                try:
                    response = requests.get(health_check_url)
                    link['health'] = response.status_code == 200
                except requests.exceptions.RequestException:
                    link['health'] = False
            else:
                link['health'] = None  # Usuń klucz `health` dla linków bez health-check

# Funkcja sprawdzająca czy plik ikony istnieje w folderze static
def icon_exists(icon_name):
   return os.path.exists(os.path.join(app.static_folder, "icons", icon_name))

@app.route('/')
def index():
   check_health_status()
   sections = config.get('sections', [])
   fallback_icon = config['fallbackIcon']['name']

   # Sprawdzanie ikon dla sekcji i linków
   for section in sections:
       section_icon = section.get('icon', '').strip()  # Pobieranie ikony sekcji i usuwanie białych znaków
       if not section_icon or not icon_exists(section_icon):
           section['icon'] = fallback_icon  # Użyj ikony zastępczej, jeśli ikona jest pusta lub nie istnieje

       for link in section.get('links', []):
           link_icon = link.get('icon', '').strip()  # Pobieranie ikony linku i usuwanie białych znaków
           if not link_icon or not icon_exists(link_icon):
               link['icon'] = fallback_icon  # Użyj ikony zastępczej, jeśli ikona jest pusta lub nie istnieje

   search = config.get('search', {})
   return render_template('index.html', sections=sections, search=search)

if __name__ == '__main__':
   app.run(debug=True)

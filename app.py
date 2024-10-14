import os
from flask import Flask, render_template

app = Flask(__name__)

# Definicja konfiguracji w słowniku
config = {
    'sections': [
        {
            'name': "Filmy i seriale",
            'icon': "films.jpg",
            'links': [
                {
                    'name': "Netflix (Filmy)",
                    'href': "https://www.netflix.com/",
                    'icon': "netflix.png"
                },
                {
                    'name': "Youtube",
                    'href': "https://www.youtube.com/",
                    'icon': "youtube.png"
                }
            ]
        },
        {
            'name': "Banki",
            'icon': "bank.png",
            'links': [
                {
                    'name': "PKO",
                    'href': "https://www.pkobp.pl",
                    'icon': "bank.png"
                },
                {
                    'name': "Millenium",
                    'href': "https://www.bankmillennium.pl",
                    'icon': "bank.png"
                }
            ]
        },
        {
            'name': "Social Media",
            'icon': "social.png",
            'links': [
                {
                    'name': "Facebook",
                    'href': "https://www.facebook.com",
                    'icon': ""
                },
                {
                    'name': "X (Twitter)",
                    'href': "https://www.twitter.com",
                    'icon': "social.png"
                }
            ]
        }
    ],
    'search': {
        'placeholder': "Search the web...",
        'name': "Google",
        'url': "https://www.google.com/search"
    },
    'fallbackIcon': {
        'name': "search.jpg"
    }
}

# Funkcja sprawdzająca czy plik ikony istnieje w folderze static
def icon_exists(icon_name):
    return os.path.exists(os.path.join(app.static_folder, "icons", icon_name))

@app.route('/')
def index():
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

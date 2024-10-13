import os
from flask import Flask, render_template, jsonify
import yaml

app = Flask(__name__)

# Liveness check: check if the application is alive
@app.route('/live')
def liveness():
    response = {
        "status": "alive",
        "message": "The application is running!"
    }
    return jsonify(response), 200

# Load the YAML config file
with open('config.yaml', 'r') as file:
   config = yaml.safe_load(file)

# Function to check if a file exists in the static folder
def icon_exists(icon_name):
   return os.path.exists(os.path.join(app.static_folder, "icons", icon_name))

@app.route('/')
def index():
   sections = config.get('sections', [])
   fallback_icon = config['fallbackIcon']['name']

   # Check icons for sections and links
   for section in sections:
       section_icon = section.get('icon', '').strip()  # Get section icon and remove whitespace
       if not section_icon or not icon_exists(section_icon):
           section['icon'] = fallback_icon  # Use fallback if icon is missing or empty

       for link in section.get('links', []):
           link_icon = link.get('icon', '').strip()  # Get link icon and remove whitespace
           if not link_icon or not icon_exists(link_icon):
               link['icon'] = fallback_icon  # Use fallback if icon is missing or empty

   search = config.get('search', {})
   return render_template('index.html', sections=sections, search=search)

if __name__ == '__main__':
   app.run(debug=True)

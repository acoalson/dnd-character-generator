"""
Flask microservice that proxies the public D&D 5e API for races and classes.
Current behavior: minimal error handling (prints status on failure, returns nothing).
Future improvements: add timeouts/retries, structured error responses, basic caching, and health endpoints.
"""
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# sends all races
races = {"races": ["dragonborn","dwarf","elf","gnome","half-elf","half-orc","halfling","human","tiefling"]}
@app.route('/get_races', methods=['POST'])
def get_races():
    """Proxy list of D&D races from upstream API and return upstream JSON on success.
    Returns: dict (200) from GET https://www.dnd5eapi.co/api/races/
    On failure: prints status to stdout and returns nothing (client should handle).
    """
    class_url = "https://www.dnd5eapi.co/api/races/"
    # Make a GET request to the API
    response = requests.get(class_url)
    print(response)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        races = response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
    return races


@app.route('/get_race_info', methods=['POST'])
def get_race_info():
    """Proxy details for a specific race.
    Body JSON: { 'race': <race_index> }  e.g., {"race": "elf"}
    Returns: dict (200) from GET https://www.dnd5eapi.co/api/races/{race}
    On failure: prints status to stdout and returns nothing.
    """
    data = request.json
    race_name = data.get('race', 'error')
    api_url = f"https://www.dnd5eapi.co/api/races/{race_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
    return
    

#sends all classes
classes = {"classes": ["barbarian","bard","cleric","druid","fighter","monk","paladin","ranger","rogue","sorcerer","warlock","wizard"]}
@app.route('/get_classes', methods=['POST'])
def get_classes():
    """Proxy list of D&D classes from upstream API and return upstream JSON on success.
    Returns: dict (200) from GET https://www.dnd5eapi.co/api/classes/
    On failure: prints status to stdout and returns nothing.
    """
    class_url = "https://www.dnd5eapi.co/api/classes/"
    # Make a GET request to the API
    response = requests.get(class_url)
    print(response)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a Python dictionary
        classes = response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
    return classes

# TODO hardcode class info
@app.route('/get_class_info', methods=['POST'])
def get_class_info():
    """Proxy details for a specific class.
    Body JSON: { 'class': <class_index> }  e.g., {"class": "wizard"}
    Returns: dict (200) from GET https://www.dnd5eapi.co/api/classes/{class}
    On failure: prints status to stdout and returns nothing.
    """
    data = request.json
    class_name = data.get('class', 'error')
    api_url = f"https://www.dnd5eapi.co/api/classes/{class_name}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
    return


    

if __name__ == '__main__':
    app.run(debug=True)

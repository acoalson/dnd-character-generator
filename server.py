from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# sends all races
races = {"races": ["dragonborn","dwarf","elf","gnome","half-elf","half-orc","halfling","human","tiefling"]}
@app.route('/get_races', methods=['POST'])
def get_races():
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

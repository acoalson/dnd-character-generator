# dnd-character-generator

# D&D API Microservice

## Overview

This microservice provides endpoints to programmatically access information about Dungeons & Dragons (D&D) races and classes through the [D&D 5e API](https://www.dnd5eapi.co/). You can make API calls to retrieve lists of races and classes, as well as detailed information about specific races and classes.

## Getting Started

To use this microservice, follow the instructions below.

### Prerequisites

- Python installed (version 3.x)
- Flask installed (`pip install flask`)
- Requests library installed (`pip install requests`)

### Starting the Microservice

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/dnd-api-microservice.git
   ```

2. Change into the project directory:

  ```bash
  cd dnd-api-microservice
  ```
  
3. Run the Flask microservice:

   ```bash
   python server.py
   ```

The microservice will be running at http://localhost:5000 or http://127.0.0.1:5000/

## API Endpoints

### 1. Get All Races
Endpoint: /get_races <br />
Method: POST <br />
Description: Retrieves a list of all D&D races. <br />
Example Request: 
```bash
data = {'race': 'elf'}
requests.post('http://127.0.0.1:5000/'+'get_race_info', json=data)
```

### 2. Get Race Information
Endpoint: /get_race_info <br />
Method: POST <br />
Description: Retrieves detailed information about a specific D&D race. <br />
Parameters: <br />
* race (string): The name of the race.

### 3. Get All Classes
Endpoint: /get_classes <br />
Method: POST <br />
Description: Retrieves a list of all D&D classes.

### 4. Get Class Information
Endpoint: /get_class_info <br />
Method: POST <br />
Description: Retrieves detailed information about a specific D&D class. <br />
Parameters: <br />
* class (string): The name of the class.

### 5. Format Race Description
Endpoint: /format_race_description <br />
Method: POST <br />
Description: Formats race based on alignment, age, size, and languages

## Receiving Data
Once a POST request is sent to [server.py](http://server.py), the response is handled by checking for success and processing the returned JSON data.
- Check the Status Code: response.status_code contains the HTTP status code returned by the microservice. A status code of 200 typically indicates a successful request.
- Retrieve JSON Data: If the status code is 200, response.json() is used to parse the JSON data returned by the microservice.

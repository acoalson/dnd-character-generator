# D&D Character Generator (Microservice + CLI)

Interactive CLI that builds a D&D 5e character using a Flask microservice which proxies the public D&D 5e API.

## Overview
- `server.py`: Flask microservice exposing race/class endpoints (proxies `https://www.dnd5eapi.co/api`).
- `client.py`: Interactive terminal app that calls the microservice to guide character creation (race, class, proficiencies, ability rolls).

## Prerequisites
- Python 3.9+
- Install deps:
  ```bash
  pip install -r requirements.txt
  ```
  If you don't have a requirements file, install directly:
  ```bash
  pip install flask requests
  ```

## Run
1) Start the microservice:
   ```bash
   python server.py
   ```
   Service listens on `http://127.0.0.1:5000`.

2) In a second terminal, start the CLI:
   ```bash
   python client.py
   ```

## API (server.py)
Base URL: `http://127.0.0.1:5000`

- GET ALL RACES
  - Endpoint: `/get_races`
  - Method: `POST`
  - Response (200): JSON from D&D API `GET /api/races`
  - Example (Python):
    ```python
    requests.post('http://127.0.0.1:5000/get_races', json={})
    ```

- GET RACE INFO
  - Endpoint: `/get_race_info`
  - Method: `POST`
  - Body: `{ "race": "elf" }`
  - Response (200): JSON from D&D API `GET /api/races/{race}`
  - Example:
    ```python
    requests.post('http://127.0.0.1:5000/get_race_info', json={"race": "elf"})
    ```

- GET ALL CLASSES
  - Endpoint: `/get_classes`
  - Method: `POST`
  - Response (200): JSON from D&D API `GET /api/classes`
  - Example:
    ```python
    requests.post('http://127.0.0.1:5000/get_classes', json={})
    ```

- GET CLASS INFO
  - Endpoint: `/get_class_info`
  - Method: `POST`
  - Body: `{ "class": "wizard" }`
  - Response (200): JSON from D&D API `GET /api/classes/{class}`
  - Example:
    ```python
    requests.post('http://127.0.0.1:5000/get_class_info', json={"class": "wizard"})
    ```

Notes:
- Endpoints proxy upstream and return the upstream JSON on success.
- On failure, the service prints an error to stdout and returns nothing (current behavior). Consider improving with structured errors.

## CLI (client.py)
- Guided UI with headers, steps, and clear prompts
- Race and class selection with numbered options, help views, and randomization
- Proficiency selection supports comma-separated input, `ls` to reprint, and `rand` to auto-fill
- Ability score rolling (4d6 drop lowest) with tidy output
- Final character summary (race, class, proficiencies, stats)

## Project Goals (Microservice Focus)
- Demonstrate a client consuming a simple domain microservice
- Encapsulate external API behind your service contract
- Provide a basis for enhancements: caching, retries, health checks, OpenAPI docs

## Suggested Enhancements
- Add timeouts, retries with backoff, and structured error responses
- Introduce `/health` and `/ready` endpoints
- Add simple caching to reduce upstream calls
- Document the API with OpenAPI (Swagger) and include examples
- Write unit tests (e.g., proficiencies parser, ability roller) and basic integration tests

## Contributing / Development
- Run code formatters/linters before PRs
- Keep user-facing messages consistent with the current UI style
- Prefer small, focused PRs (UI, service behavior, tests) with brief summaries

## License
MIT (or your chosen license)

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WINDOW_SIZE = 10
WINDOW = []

TOKEN = os.getenv("API_TOKEN")


def fetch_numbers_from_server(numberid):
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    try:
        if numberid == 'p':
            response = requests.get(f'http://20.244.56.144/test/primes', headers=headers, timeout=0.5)
            response.raise_for_status()
            return response.json().get('numbers', [])
        if numberid == 'e':
            response = requests.get(f'http://20.244.56.144/test/even', headers=headers, timeout=0.5)
            response.raise_for_status()
            return response.json().get('numbers', [])
        if numberid == 'f':
            response = requests.get(f'http://20.244.56.144/test/fibo', headers=headers, timeout=0.5)
            response.raise_for_status()
            return response.json().get('numbers', [])
        if numberid == 'r':
            response = requests.get(f'http://20.244.56.144/test/rand', headers=headers, timeout=0.5)
            response.raise_for_status()
            return response.json().get('numbers', [])
    except requests.RequestException as e:
        print(f"Failed to fetch data from server: {e}")
        return []

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    numbers = fetch_numbers_from_server(numberid)

    global WINDOW
    previous_state = WINDOW.copy()

    for number in numbers:
        if number not in WINDOW:
            if len(WINDOW) >= WINDOW_SIZE:
                WINDOW.pop(0)
            WINDOW.append(number)

    current_state = WINDOW
    average = sum(current_state) / len(current_state) if current_state else 0

    response = {
        "numbers": numbers,
        "windowPrevState": previous_state,
        "windowCurrState": current_state,
        "average": average
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

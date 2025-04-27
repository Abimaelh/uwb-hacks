from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
from model import gemma_container
HOST = 'localhost'
PORT = '5000'
server = Flask(__name__)
CORS(server)

def APIret(keywords):
    query = " ".join(keywords)  # Combines keywords into one search string

    headers = {
        "X-API-KEY": "cd0c021e-07d6-4456-88aa-4133a34e29fc"
    }

    params = {
        "q": query,
        "jurisdiction": "California",  # optional
        "per_page": 10
    }

    response = requests.get("https://v3.openstates.org/bills", headers=headers, params=params)
    data = response.json()

    for bill in data.get("results", []):
        print(f"{bill['identifier']}: {bill['title']}, {bill['subject']}")

@server.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print("Received message:", data['message'])

    topics = gemma_container.extractTopics(data['message'])
    

    return jsonify({
        'summMessage': 'This is your AI summary!',
        'source': 'Python backend'
    })


if __name__ == "__main__":
    server.run(host=HOST, port=PORT)
    keywords = ["homeless", "shelter"]

    spit = APIret(keywords)
    print(spit)
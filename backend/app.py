from flask import Flask
from models import db
from routes import bp

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS

import requests

keywords = ["homeless", "shelter"]

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
    print(f"{bill['identifier']}: {bill['title']}, {bill['classification']}")

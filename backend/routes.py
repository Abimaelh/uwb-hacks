from flask import Blueprint, request, jsonify
from DBModel import db, Interest
from model import gemma_container
import requests

bp = Blueprint('api', __name__)

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
    return data

@bp.route('/submit', methods=['POST'])
def submit_interest():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Extract topics using gemma_container
    topics = gemma_container.extractTopics(message)

    # Fetch API results using the extracted topics
    api_results = APIret(topics)

    # Optionally, save topics to the database
    city = data.get('city', 'Unknown')
    state = data.get('state', 'Unknown')
    for topic in topics:
        new_interest = Interest(city=city.strip(), state=state.strip(), topic=topic.strip().lower())
        db.session.add(new_interest)
    db.session.commit()

    return jsonify({
        "message": "Thank you for making your voice heard!",
        "topics": topics,
        "apiResults": api_results
    }), 201

@bp.route('/community-interests', methods=['GET'])
def get_community_interests():
    results = {}
    all_interests = Interest.query.all()

    for interest in all_interests:
        loc = f"{interest.city}, {interest.state}"
        if loc not in results:
            results[loc] = []
        results[loc].append(interest.topic)

    # Now, count and show top topics per location
    summarized = {}
    for loc, topics in results.items():
        counter = {}
        for topic in topics:
            counter[topic] = counter.get(topic, 0) + 1
        top_topics = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        summarized[loc] = [topic for topic, count in top_topics[:5]]  # Top 5 issues

    return jsonify(summarized), 200
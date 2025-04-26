from flask import Blueprint, request, jsonify
from DBModel import db, Interest

bp = Blueprint('api', __name__)

@bp.route('/submit', methods=['POST'])
def submit_interest():
    data = request.get_json()
    city = data.get('city')
    state = data.get('state')
    topics = data.get('topics')  # This should be a list

    if not city or not state or not topics:
        return jsonify({"error": "Missing fields"}), 400

    for topic in topics:
        new_interest = Interest(city=city.strip(), state=state.strip(), topic=topic.strip().lower())
        db.session.add(new_interest)

    db.session.commit()
    return jsonify({"message": "Thank you for making your voice heard!"}), 201

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
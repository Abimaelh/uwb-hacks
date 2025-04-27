from flask import Flask, request, jsonify
from flask_cors import CORS
from model import gemma_container
import time

import requests
from model import gemma_container
HOST = 'localhost'
PORT = '5000'
server = Flask(__name__)
CORS(server)

def APIret(topics):
    
    print("Extracted Topics:", topics)

    if topics:
        headers = {
        "X-API-KEY": "cd0c021e-07d6-4456-88aa-4133a34e29fc"
    }

        endpoints = {
            "bills": "https://v3.openstates.org/bills",
            "people": "https://v3.openstates.org/people"
            # "organizations": "https://v3.openstates.org/organizations",
            # "events": "https://v3.openstates.org/events",
            # "votes": "https://v3.openstates.org/votes"
        }

        collected_results = {}

        for topic in topics:
            print(f"\nSearching for topic: '{topic}'")

            for entity, url in endpoints.items():
                params = {
                    "q": topic,
                    "per_page": 5,  # limit per topic/entity to avoid huge data
                    "jurisdiction": "Washington"
                }

                try:
                    response = requests.get(url, headers=headers, params=params)
                    response.raise_for_status()
                    data = response.json()

                    # If there are results, store them
                    if data.get("results"):
                        if topic not in collected_results:
                            collected_results[topic] = {}
                        collected_results[topic][entity] = data["results"]

                    # time.sleep(0.2)

                except Exception as e:
                    pass
                    # print(f"Error fetching {entity} for topic '{topic}': {e}")

    # return collected_results
    return collected_results

@server.route('/submit', methods=['POST'])
def submit():
    # data = request.get_json()
    # print("Received message:", data['message'])
    
    # return jsonify({
    #     'summMessage': 'This is your AI summary!',
    #     'source': 'Python backend'
    # })
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Extract topics using gemma_container
    topics = gemma_container.extractTopics(message)

    print("Fetching API results")
    # Fetch API results using the extracted topics
    api_results = APIret(topics)

    #pretty_results = results_to_string(api_results)

    # Summarise results of the topics
    summary = gemma_container.summarizeDatabaseReturn("\n".join(api_results))

    return jsonify({
        "message": "Thank you for making your voice heard!",
        "topics": topics,
        "source": " ", #pretty_results
        "summMessage": summary
    }), 201

def results_to_string(collected_results):
    output_lines = []

    for topic, topic_data in collected_results.items():
        output_lines.append(f"🔹 Results for Topic: '{topic}'")
        for entity, items in topic_data.items():
            output_lines.append(f"  📚 {entity.capitalize()} ({len(items)} results)")
            for item in items:
                if entity == "bills":
                    line = f"    - [Bill {item.get('identifier', '')}] {item.get('title', '')}"
                elif entity == "people":
                    role = item.get('current_role', {}).get('title', 'Unknown Role')
                    line = f"    - [Person] {item.get('name', '')} ({role})"
                elif entity == "organizations":
                    line = f"    - [Organization] {item.get('name', '')}"
                elif entity == "events":
                    date = item.get('start_date', 'Unknown Date')
                    line = f"    - [Event] {item.get('name', '')} on {date}"
                elif entity == "votes":
                    bill_id = item.get('bill', {}).get('identifier', 'Unknown Bill')
                    motion = item.get('motion_text', '')
                    line = f"    - [Vote] {bill_id} - {motion}"
                else:
                    line = f"    - [Unknown Entity] {str(item)}"

                output_lines.append(line)

    # Join everything into one big string
    return "\n".join(output_lines)


if __name__ == "__main__":
    server.run(host=HOST, port=PORT)
    # keywords = ["homeless", "shelter"]

    # input_text = "Homelessness and electric bills in Seattle, as well as rising healthcare costs."
    # topics = gemma_container.extractTopics(input_text)

    # listings = APIret(topics)
    # print(listings)
    # # listings
    # print("\n")

    # spit = gemma_container.summarizeDatabaseReturn(listings)
    # print(spit)
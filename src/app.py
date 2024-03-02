from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL of the deployed RAG model on GCP
RAG_MODEL_URL = "http://<your-gcp-rag-model-endpoint>/predict"

# Kafka Producer for sending questions
# producer = KafkaProducer(bootstrap_servers=['your_kafka_server:9092'],
#                          value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Kafka Consumer for receiving answers
# consumer = KafkaConsumer('answer_topic',
#                          bootstrap_servers=['your_kafka_server:9092'],
#                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    # Send the question to the deployed RAG model
    response = requests.post(RAG_MODEL_URL, json={'question': question})

    if response.status_code == 200:
        # Assuming the RAG model endpoint returns a JSON with an 'answer' key
        answer = response.json().get('answer', 'No answer provided.')
        return jsonify({'question': question, 'answer': answer})
    else:
        return jsonify({'error': 'Failed to get an answer from the RAG model'}), 500

@app.route("/health")
def health():
    return "<h1>Server working fine</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

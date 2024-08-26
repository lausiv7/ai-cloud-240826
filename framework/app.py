from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LLM_URL = 'http://llm:5000'  # llm service URL in Docker Compose

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Forward the question to the LLM service
    response = requests.post(f"{LLM_URL}/infer", json={"question": question})
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to get response from LLM service"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

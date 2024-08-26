from flask import Flask, request, jsonify
from model import generate_response

app = Flask(__name__)

@app.route('/infer', methods=['POST'])
def infer():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Generate response using the LLM
    response = generate_response(question)
    
    return jsonify({"response": response})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "LLM service is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Define the base URL format for LLM services
LLM_URL_TEMPLATE = "http://llm_{index}:5000"

@app.route('/')
def index():
    llm_count = int(request.args.get('llm_count', 3))  # You can change the default count based on your setup
    return render_template('index.html', llm_count=llm_count)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')
    llm_index = request.json.get('llm_index', 0)  # Default to the first LLM

    llm_url = LLM_URL_TEMPLATE.format(index=llm_index)

    try:
        response = requests.post(f"{llm_url}/infer", json={"question": question})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

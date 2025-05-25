from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that explains cybersecurity concepts clearly."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"⚠️ Error: {str(e)}"})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "⚠️ No file provided."})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "⚠️ Empty filename."})

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    return jsonify({"message": f"✅ File '{file.filename}' uploaded successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

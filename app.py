from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

API_KEY = os.getenv("GROQ_API_KEY", "")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    if not API_KEY:
        return jsonify({"response": "⚠️ API key not configured. Please set GROQ_API_KEY in .env file."})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that explains cybersecurity concepts clearly."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 400:
            error_detail = response.json().get('error', {}).get('message', 'Bad request')
            return jsonify({"response": f"⚠️ Bad request: {error_detail}"})
        elif response.status_code == 429:
            return jsonify({"response": "⚠️ API rate limit exceeded. Please try again later."})
        elif response.status_code == 401:
            return jsonify({"response": "⚠️ Invalid API key. Please check your GROQ_API_KEY."})
        elif response.status_code == 403:
            return jsonify({"response": "⚠️ Access forbidden. Please check your API key permissions."})
        
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})
    except requests.exceptions.Timeout:
        return jsonify({"response": "⚠️ Request timed out. Please try again."})
    except requests.exceptions.RequestException as e:
        return jsonify({"response": f"⚠️ Network error: {str(e)}"})
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

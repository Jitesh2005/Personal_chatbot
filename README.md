# Personal Chatbot

A Flask-based security chatbot with file upload and camera capture features.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a FREE Groq API key:
   - Go to [Groq Console](https://console.groq.com/keys)
   - Sign up (it's free!)
   - Create a new API key
   - Copy the key

3. Configure your API key:
   - Open `.env` file
   - Replace `your_groq_api_key_here` with your actual key

4. Run the app:
```bash
python app.py
```

5. Open browser to `http://127.0.0.1:5000`

## Features

- Chat with AI (powered by Llama 3.1 70B)
- Upload files
- Capture photos from camera
- Cybersecurity focused responses

## Troubleshooting

- **Rate limit errors**: Free tier has limits. Wait a bit and try again.
- **401 errors**: Invalid API key. Check your `.env` file.
- **No response**: Make sure you set your GROQ_API_KEY in `.env`
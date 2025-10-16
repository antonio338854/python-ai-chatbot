"""
Web-based Chatbot using Flask
Run with: python web_chatbot.py
Access at: http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

class WebChatBot:
    """Web-enabled chatbot"""
    def __init__(self):
        self.conversation_history = []
        self.responses = {
            "greeting": "Olá! Como posso ajudar?",
            "help": "Poso responder perguntas e manter uma conversa.",
            "default": "Entendo. Pode detalhar mais?"
        }
    
    def get_intent(self, text):
        text_lower = text.lower()
        if any(word in text_lower for word in ["oi", "olá", "hey"]):
            return "greeting"
        if any(word in text_lower for word in ["ajuda", "help"]):
            return "help"
        return "default"
    
    def process(self, user_input):
        intent = self.get_intent(user_input)
        response = self.responses[intent]
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "bot": response
        })
        
        return response

bot = WebChatBot()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Chatbot API", "version": "1.0"})
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        response = bot.process(user_input)
        return jsonify({
            "user_message": user_input,
            "bot_response": response,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": bot.conversation_history})
@app.route("/history", methods=["DELETE"])
def clear_history():
    bot.conversation_history = []
    return jsonify({"message": "History cleared"})

if __name__ == "__main__":
    print("Starting AI Chatbot Web Server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
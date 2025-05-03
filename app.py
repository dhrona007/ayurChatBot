from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
import brain
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable is not set.")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "meta-llama/Llama-3-70b-chat-hf"

class Assessment:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.scores = {'vata': 0, 'pitta': 0, 'kapha': 0}
        self.responses = []
    
    def update_scores(self, answer):
        if answer in brain.ans_1:
            self.scores['vata'] += 1
        elif answer in brain.ans_2:
            self.scores['pitta'] += 1
        elif answer in brain.ans_3:
            self.scores['kapha'] += 1

# Store active assessments
active_assessments = {}

# Assessment Endpoints
@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all assessment questions"""
    questions = [{
        'id': idx,
        'text': q,
        'options': list(set(brain.ans_1 + brain.ans_2 + brain.ans_3))
    } for idx, q in enumerate(brain.questions)]
    return jsonify(questions)

@app.route('/api/assess', methods=['POST'])
def process_answer():
    """Process user's answer and update scores"""
    data = request.json
    session_id = data.get('session_id')
    answer = data['answer'].lower()
    
    if session_id not in active_assessments:
        active_assessments[session_id] = Assessment()
    
    assessment = active_assessments[session_id]
    assessment.update_scores(answer)
    
    return jsonify({
        'scores': assessment.scores,
        'next_question': len(assessment.responses) + 1
    })

# Chat Endpoints
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with Together AI integration"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    try:
        # Prepare messages for Together AI
        messages = [{
            "role": "system",
            "content": """You are an Ayurvedic expert assistant. Provide:
            - Clear explanations of doshas (vata, pitta, kapha)
            - Personalized health recommendations
            - Lifestyle and diet advice
            - Answers in simple, friendly language, format the responses properly
            - Maximum 1-2 sentences per response"""
        }]
        
        # Add chat history
        for msg in session['chat_history'][-6:]:  # Keep last 6 messages for context
            messages.append({
                "role": "user" if msg['sender'] == 'user' else "assistant",
                "content": msg['message']
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Call Together AI API
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": TOGETHER_MODEL,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 150
        }
        
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for bad status codes
        
        bot_response = response.json()['choices'][0]['message']['content']
        
        # Update session history
        session['chat_history'].extend([
            {'sender': 'user', 'message': user_message},
            {'sender': 'bot', 'message': bot_response}
        ])
        session.modified = True
        
        return jsonify({'response': bot_response})
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Together AI API error: {str(e)}")
        return jsonify({
            'response': "I'm having trouble connecting to the knowledge base. "
                       "You can try again later or begin the assessment for "
                       "personalized recommendations."
        }), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'response': "An unexpected error occurred. Please try again."
        }), 500


@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get the user's chat history"""
    return jsonify(session.get('chat_history', []))

@app.route('/api/chat/clear', methods=['POST'])
def clear_chat_history():
    """Clear the chat history"""
    session['chat_history'] = []
    session.modified = True
    return jsonify({'status': 'success'})

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Service health check"""
    return jsonify({
        'status': 'healthy',
        'openai_ready': bool(TOGETHER_API_KEY),
        'assessment_questions': len(brain.questions)
    })

# Serve frontend static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

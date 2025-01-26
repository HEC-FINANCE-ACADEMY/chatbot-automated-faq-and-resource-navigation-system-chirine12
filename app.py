from flask import Flask, request, jsonify, render_template
from utils.chatbot import main, recommend_program_based_on_interests, speak_text_auto
import json

app = Flask(__name__)

# Charger les données JSON
with open("dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if "programme me convient" in user_input.lower() or "suitable program" in user_input.lower():
        return jsonify({"response": "Je peux vous aider à trouver le programme qui correspond le mieux à vos intérêts. Pouvez-vous me dire ce qui vous passionne ou les domaines dans lesquels vous aimeriez travailler ?"})
    
    elif "intérêts" in user_input.lower() or "interests" in user_input.lower():
        interests = user_input
        program, description = recommend_program_based_on_interests(interests)
        if program:
            response = f"En fonction de vos intérêts, je vous recommande le programme en *{program}*. {description}"
            speak_text_auto(response)
            return jsonify({"response": response})
        else:
            response = "Désolé, je n'ai pas trouvé de programme correspondant à vos intérêts."
            speak_text_auto(response)
            return jsonify({"response": response})
    
    else:
        # Utiliser le chatbot pour répondre à la requête
        response = main(user_input)
        speak_text_auto(response)
        return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
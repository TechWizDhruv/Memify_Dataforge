from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API with basic settings
GOOGLE_API_KEY = "API KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# Print available models for debugging
print("Available models:", [m.name for m in genai.list_models()])

# Initialize the model with the new recommended version
model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-caption', methods=['POST'])
def generate_caption():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        # Create structured content with specific instructions
        response = model.generate_content(
            "You are a meme caption generator. Create a funny, short caption for this scenario: " + prompt
        )
        
        if response and hasattr(response, 'text'):
            return jsonify({"caption": response.text.strip(), "success": True})
        else:
            return jsonify({"error": "No caption generated", "success": False}), 400
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging for debugging
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True)


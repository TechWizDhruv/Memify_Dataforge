"""
MemeMind Web Interface Module

This module provides a Flask web interface for the MemeMind meme generator.
"""

import os
import uuid
from flask import Flask, request, render_template, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from nlp.analyzer import NLPAnalyzer
from meme.generator import MemeGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '../meme/output')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize NLP analyzer and meme generator
nlp_analyzer = NLPAnalyzer()
meme_generator = MemeGenerator()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    API endpoint to analyze text without generating a meme.
    
    Returns JSON with NLP analysis results.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    # Analyze the text
    analysis_result = nlp_analyzer.analyze(text)
    
    return jsonify(analysis_result)

@app.route('/api/generate-meme', methods=['POST'])
def generate_meme():
    """
    API endpoint to generate a meme from input text.
    
    Returns JSON with the meme image URL and analysis results.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    
    # Analyze the text
    analysis_result = nlp_analyzer.analyze(text)
    
    # Get meme parameters from analysis
    meme_params = nlp_analyzer.get_meme_parameters(analysis_result)
    
    # Generate a meme
    filename = f"meme_{uuid.uuid4().hex[:8]}.jpg"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    meme_path = meme_generator.create_meme(meme_params, output_path)
    
    # Create URL for the meme
    meme_url = url_for('serve_meme', filename=os.path.basename(meme_path))
    
    return jsonify({
        'meme_url': meme_url,
        'analysis': analysis_result
    })

@app.route('/memes/<filename>')
def serve_meme(filename):
    """Serve generated meme images."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/templates', methods=['GET'])
def list_templates():
    """
    API endpoint to list available meme templates.
    
    Returns JSON with template names and URLs.
    """
    templates_dir = meme_generator.templates_dir
    template_files = [f for f in os.listdir(templates_dir) 
                     if os.path.isfile(os.path.join(templates_dir, f)) 
                     and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    templates = []
    for template in template_files:
        templates.append({
            'name': template,
            'url': url_for('serve_template', filename=template)
        })
    
    return jsonify({'templates': templates})

@app.route('/templates/<filename>')
def serve_template(filename):
    """Serve meme template images."""
    return send_from_directory(meme_generator.templates_dir, filename)

if __name__ == '__main__':
    app.run(debug=True) 
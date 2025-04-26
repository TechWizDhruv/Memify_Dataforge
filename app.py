#!/usr/bin/env python
"""
MemeMind: AI-Powered Meme Generator

This is the main entry point for the MemeMind application.
"""

import os
import sys
import nltk
from web.app import app

def setup_resources():
    """
    Set up necessary resources for the application.
    
    Downloads required NLTK data and spaCy models if not already present.
    """
    print("Setting up resources...")
    
    # Create necessary directories
    os.makedirs("meme/templates", exist_ok=True)
    os.makedirs("meme/output", exist_ok=True)
    
    # Download NLTK resources
    print("Setting up NLTK resources...")
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords')
    
    try:
        nltk.data.find('sentiment/vader_lexicon')
    except LookupError:
        print("Downloading NLTK VADER lexicon...")
        nltk.download('vader_lexicon')
    
    # Note: spaCy requirement is temporarily disabled
    print("Note: spaCy model download is skipped due to compatibility issues.")
    print("Some NLP features may be limited.")
    
    print("Resource setup complete.")

if __name__ == "__main__":
    # Check if we need to set up resources
    setup_flag = "--setup" in sys.argv
    if setup_flag:
        setup_resources()
    
    # Check if port is specified
    port = 5000  # Default port
    for arg in sys.argv:
        if arg.startswith("--port="):
            try:
                port = int(arg.split("=")[1])
            except:
                pass
    
    # Run the application
    print(f"Starting MemeMind on port {port}...")
    print(f"Open your browser and navigate to http://localhost:{port}/ to use the application.")
    app.run(host="0.0.0.0", port=port, debug="--debug" in sys.argv) 
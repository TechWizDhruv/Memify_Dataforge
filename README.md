# MemeMind: AI-Powered Meme Generator

An intelligent meme generator that uses NLP to analyze input topics and generate relevant, contextually appropriate memes.

## Features

- Topic-aware meme generation
- Sentiment and emotion analysis
- Cultural context understanding
- Customizable meme templates
- Web interface for easy interaction

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download required NLP models:
   ```
   python -m spacy download en_core_web_md
   python -m nltk.downloader vader_lexicon punkt stopwords wordnet
   ```
4. Run the application:
   ```
   python app.py
   ```

## Project Structure

- `app.py`: Main application entry point
- `nlp/`: NLP processing modules
  - `analyzer.py`: Core text analysis functionality
  - `sentiment.py`: Sentiment and emotion detection
  - `context.py`: Cultural context analysis
- `meme/`: Meme generation modules
  - `generator.py`: Creates memes based on NLP analysis
  - `templates/`: Meme template storage
- `web/`: Web interface components

## Usage

1. Enter a topic, headline, or idea
2. MemeMind analyzes the input using NLP
3. Appropriate meme templates are selected
4. A relevant caption is generated
5. The finished meme is presented to the user 
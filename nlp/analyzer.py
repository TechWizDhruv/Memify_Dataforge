"""
NLP Analyzer Module

This module coordinates the NLP analysis of input text for the MemeMind application.
It integrates sentiment analysis, emotion detection, cultural context analysis, and tone detection.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .sentiment import EmotionDetector
from .context import ContextAnalyzer

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class NLPAnalyzer:
    """Main class for analyzing input text and extracting features for meme generation."""
    
    def __init__(self):
        """Initialize the NLP analyzer with necessary models and components."""
        # SpaCy is temporarily disabled due to compatibility issues
        self.nlp = None
        print("Note: Using simplified NLP analysis due to spaCy compatibility issues")
            
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize simplified emotion detector and context analyzer
        self.emotion_detector = EmotionDetector()
        self.context_analyzer = ContextAnalyzer()
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess(self, text):
        """Preprocess the input text for analysis."""
        # Tokenize the text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and punctuation
        tokens = [token for token in tokens if token.isalnum() and token not in self.stop_words]
        
        # Return preprocessed text
        return " ".join(tokens)
    
    def analyze(self, text):
        """
        Analyze input text and return a comprehensive analysis.
        
        Args:
            text (str): The input text to analyze
            
        Returns:
            dict: A dictionary containing the analysis results
        """
        # Create result dictionary
        result = {
            "original_text": text,
            "sentiment": {},
            "emotions": [],
            "entities": [],
            "topics": [],
            "tone": "",
            "formality": ""
        }
        
        # Preprocess text
        preprocessed_text = self.preprocess(text)
        
        # Simple entity extraction without spaCy (just look for capitalized words)
        words = text.split()
        entities = []
        for word in words:
            if word[0].isupper() and len(word) > 1 and word.lower() not in self.stop_words:
                entities.append({"text": word, "label": "ENTITY"})
        
        result["entities"] = entities
        
        # Get VADER sentiment
        vader_sentiment = self.sentiment_analyzer.polarity_scores(text)
        result["sentiment"]["vader"] = {
            "compound": vader_sentiment["compound"],
            "positive": vader_sentiment["pos"],
            "negative": vader_sentiment["neg"],
            "neutral": vader_sentiment["neu"]
        }
        
        # Simplified transformer sentiment (fake)
        if vader_sentiment["compound"] > 0.05:
            label = "POSITIVE"
            score = vader_sentiment["pos"]
        elif vader_sentiment["compound"] < -0.05:
            label = "NEGATIVE"
            score = vader_sentiment["neg"]
        else:
            label = "NEUTRAL"
            score = vader_sentiment["neu"]
            
        result["sentiment"]["transformer"] = {
            "label": label,
            "score": score
        }
        
        # Get emotions from simplified emotion detector
        result["emotions"] = self.emotion_detector.detect_emotions(text)
        
        # Analyze context and topics with simplified approach
        # Just extract common nouns as topics
        topics = []
        for word in text.split():
            word = word.lower()
            if len(word) > 3 and word not in self.stop_words:
                if word not in [t.lower() for t in topics]:
                    topics.append(word)
        
        if len(topics) > 3:
            topics = topics[:3]  # Limit to 3 topics
            
        result["topics"] = topics
        
        # Determine formality (simplified)
        words = text.lower().split()
        formal_markers = ["therefore", "however", "thus", "hence", "nevertheless", "furthermore", "moreover"]
        informal_markers = ["lol", "haha", "yeah", "cool", "awesome", "btw", "gonna", "wanna"]
        
        formal_count = sum(1 for w in words if w in formal_markers)
        informal_count = sum(1 for w in words if w in informal_markers)
        
        result["formality"] = "formal" if formal_count > informal_count else "informal"
        
        # Determine overall tone based on combined factors
        result["tone"] = self._determine_tone(result)
        
        return result
    
    def _determine_tone(self, analysis_result):
        """
        Determine the overall tone of the text based on combined analysis factors.
        
        Args:
            analysis_result (dict): The complete analysis result
            
        Returns:
            str: The detected tone (humorous, serious, sarcastic, etc.)
        """
        # This is a simplified version - a real implementation would be more sophisticated
        
        # Check for question marks as a signal of inquisitive tone
        if "?" in analysis_result["original_text"] and "!" not in analysis_result["original_text"]:
            return "inquisitive"
            
        # Check for exclamation marks as a signal of excited tone
        if "!" in analysis_result["original_text"]:
            return "excited"
        
        # Check emotions for humor signals
        for emotion in analysis_result["emotions"]:
            if emotion["label"] == "joy" and emotion["score"] > 0.6:
                return "humorous"
            if emotion["label"] == "surprise" and emotion["score"] > 0.7:
                return "surprising"
        
        # Check sentiment for serious signals
        vader_compound = analysis_result["sentiment"]["vader"]["compound"]
        if vader_compound < -0.5:
            return "serious_negative"
        if vader_compound > 0.5:
            return "enthusiastic"
            
        # Default to neutral
        return "neutral"
    
    def get_meme_parameters(self, analysis_result):
        """
        Convert NLP analysis results into parameters for meme generation.
        
        Args:
            analysis_result (dict): The complete analysis result from the analyze method
            
        Returns:
            dict: Parameters suitable for passing to a meme generator
        """
        # Extract the most relevant emotions (top 2)
        top_emotions = sorted(
            analysis_result["emotions"], 
            key=lambda x: x["score"], 
            reverse=True
        )[:2]
        
        # Determine primary sentiment
        compound_score = analysis_result["sentiment"]["vader"]["compound"]
        if compound_score >= 0.05:
            primary_sentiment = "positive"
        elif compound_score <= -0.05:
            primary_sentiment = "negative"
        else:
            primary_sentiment = "neutral"
            
        # Extract main topic if available
        main_topic = analysis_result["topics"][0] if analysis_result["topics"] else "general"
        
        # Extract main entities if available
        main_entities = [entity["text"] for entity in analysis_result["entities"][:3]]
        
        # Compile meme parameters
        meme_params = {
            "sentiment": primary_sentiment,
            "tone": analysis_result["tone"],
            "formality": analysis_result["formality"],
            "emotions": [emotion["label"] for emotion in top_emotions],
            "topic": main_topic,
            "entities": main_entities,
            "text": analysis_result["original_text"]
        }
        
        return meme_params 
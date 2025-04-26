"""
Sentiment Analysis Module

This module handles sentiment and emotion detection for the MemeMind application.
"""

from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EmotionDetector:
    """
    Detects emotions in text using simplified keyword-based approach.
    """
    
    def __init__(self):
        """Initialize the emotion detector with emotion keyword dictionaries."""
        # Initialize the sentiment analyzer for supporting emotion detection
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Emotion keyword dictionaries
        self.emotion_keywords = {
            "joy": [
                "happy", "happiness", "joy", "joyful", "delighted", "excited", "ecstatic", 
                "thrilled", "glad", "pleased", "wonderful", "great", "awesome", "fantastic",
                "amazing", "excellent", "love", "loving", "celebrate", "celebration", "party",
                "laugh", "laughter", "smile", "smiling", "haha", "lol", "yay", "woohoo"
            ],
            "sadness": [
                "sad", "sadness", "unhappy", "depressed", "depression", "miserable", "gloomy",
                "heartbroken", "grief", "disappointed", "upset", "regret", "regretful", "sorry",
                "sorrow", "crying", "cry", "tears", "weeping", "sobbing", "hurt", "painful"
            ],
            "anger": [
                "angry", "anger", "mad", "furious", "rage", "outraged", "annoyed", "irritated",
                "frustration", "frustrated", "hate", "hatred", "resent", "resentment", "disgusted",
                "disgust", "hostile", "hostility", "bitter", "bitterness", "offended", "upset"
            ],
            "fear": [
                "afraid", "fear", "scared", "frightened", "terrified", "terror", "panic", "anxious",
                "anxiety", "nervous", "worried", "worry", "dread", "horror", "horrified", "alarmed",
                "threatened", "threatening", "danger", "dangerous", "scary"
            ],
            "surprise": [
                "surprised", "surprise", "shocked", "shock", "astonished", "astonishment", "amazed",
                "amazing", "unexpected", "startled", "stunned", "wow", "whoa", "omg", "incredible",
                "unbelievable", "unreal", "mind-blowing", "mind blown"
            ],
            "disgust": [
                "disgusted", "disgust", "gross", "revolting", "repulsed", "repulsive", "nasty",
                "sickening", "sickened", "nauseous", "offensive", "eww", "ew", "yuck", "icky"
            ],
            "confusion": [
                "confused", "confusion", "perplexed", "puzzled", "baffled", "uncertain", "unsure",
                "ambiguous", "unclear", "bewildered", "bemused", "dumbfounded", "stumped", "lost"
            ]
        }
    
    def detect_emotions(self, text):
        """
        Detect emotions in the given text using keyword matching.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            list: List of detected emotions with scores, sorted by score
        """
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Count emotion keywords
        emotion_counts = {emotion: 0 for emotion in self.emotion_keywords}
        
        for token in tokens:
            for emotion, keywords in self.emotion_keywords.items():
                if token in keywords:
                    emotion_counts[emotion] += 1
        
        # Get sentiment to help with emotion detection
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        # Adjust emotion scores based on sentiment
        if sentiment["compound"] > 0.3:
            emotion_counts["joy"] += 1
        elif sentiment["compound"] < -0.3:
            emotion_counts["sadness"] += 1
            
        if sentiment["neg"] > 0.5:
            emotion_counts["anger"] += 1
            
        # Convert counts to scores (0-1 range)
        max_count = max(max(emotion_counts.values()), 1)  # Avoid division by zero
        emotion_scores = []
        
        for emotion, count in emotion_counts.items():
            # Calculate score, ensuring some variety in results
            base_score = count / max_count
            
            # Add a small random factor to avoid ties
            score = min(base_score * 0.8 + 0.2, 1.0) if count > 0 else 0
            
            if score > 0:
                emotion_scores.append({
                    "label": emotion,
                    "score": score
                })
        
        # If no emotions detected, add a neutral emotion
        if not emotion_scores:
            emotion_scores.append({
                "label": "neutral",
                "score": 1.0
            })
        
        # Sort emotions by score (descending)
        emotion_scores.sort(key=lambda x: x["score"], reverse=True)
        
        return emotion_scores 
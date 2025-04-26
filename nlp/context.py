"""
Context Analyzer Module

This module analyzes the cultural and contextual aspects of text for the MemeMind application.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ContextAnalyzer:
    """Analyzes cultural context and topics in text."""
    
    def __init__(self):
        """Initialize the context analyzer."""
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Simplified topic detection
        self.topic_keywords = {
            "politics": ["government", "president", "election", "vote", "democracy", "political", "party", "senator", "congress", "law"],
            "technology": ["computer", "software", "hardware", "code", "programming", "tech", "digital", "internet", "app", "website", "algorithm"],
            "entertainment": ["movie", "film", "tv", "television", "actor", "actress", "show", "series", "music", "song", "celebrity"],
            "sports": ["game", "team", "player", "football", "soccer", "basketball", "baseball", "sport", "win", "lose", "score"],
            "business": ["money", "finance", "investment", "stock", "market", "company", "corporation", "ceo", "profit", "economic"],
            "science": ["research", "scientist", "experiment", "theory", "physics", "biology", "chemistry", "scientific", "laboratory"],
            "social_media": ["facebook", "twitter", "instagram", "tiktok", "viral", "post", "share", "like", "follow", "social"],
            "memes": ["meme", "funny", "joke", "humor", "lol", "viral", "reddit", "trend", "dank"]
        }
        
        # Formality detection
        self.formal_markers = [
            "therefore", "however", "thus", "hence", "nevertheless", "furthermore", "moreover",
            "accordingly", "consequently", "subsequently", "although", "despite", "whereas",
            "notwithstanding", "regarding", "concerning", "hereby", "herein", "pursuant",
            "shall", "must", "require", "necessitate"
        ]
        
        self.informal_markers = [
            "lol", "haha", "yeah", "cool", "awesome", "btw", "gonna", "wanna",
            "kinda", "sorta", "yep", "nope", "dude", "like", "totally", "stuff",
            "u", "ur", "r", "y", "k", "omg", "wtf", "idk", "tbh", "imo"
        ]
    
    def analyze(self, text, doc=None):
        """
        Analyze the cultural context of the text.
        
        Args:
            text (str): The text to analyze
            doc: Optional pre-processed spaCy doc (not used in the simplified version)
            
        Returns:
            dict: Analysis results including topics and formality
        """
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        
        # Detect topics
        topics = self._detect_topics(filtered_tokens)
        
        # Detect formality
        is_formal = self._detect_formality(tokens)
        
        return {
            "topics": topics,
            "is_formal": is_formal
        }
    
    def _detect_topics(self, tokens):
        """
        Detect topics in the text based on keyword matching.
        
        Args:
            tokens (list): List of tokens to analyze
            
        Returns:
            list: Detected topics
        """
        # Count occurrences of topic keywords
        topic_counts = {topic: 0 for topic in self.topic_keywords}
        
        for token in tokens:
            for topic, keywords in self.topic_keywords.items():
                if token in keywords:
                    topic_counts[topic] += 1
        
        # Get the top topics (those with at least one keyword)
        topics = [topic for topic, count in topic_counts.items() if count > 0]
        topics.sort(key=lambda t: topic_counts[t], reverse=True)
        
        # If no specific topics were found, use "general"
        if not topics:
            topics = ["general"]
        
        return topics[:3]  # Return top 3 topics max
    
    def _detect_formality(self, tokens):
        """
        Detect the formality level of the text.
        
        Args:
            tokens (list): List of tokens to analyze
            
        Returns:
            bool: True if formal, False if informal
        """
        # Count formal and informal markers
        formal_count = sum(1 for token in tokens if token.lower() in self.formal_markers)
        informal_count = sum(1 for token in tokens if token.lower() in self.informal_markers)
        
        # Consider sentence structure
        sentences = nltk.sent_tokenize(" ".join(tokens))
        avg_sentence_length = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences) / len(sentences) if sentences else 0
        
        # Weighted decision - formality is influenced by:
        # 1. Presence of formal markers
        # 2. Absence of informal markers
        # 3. Longer sentences (on average)
        formality_score = formal_count * 2 - informal_count * 1.5 + (avg_sentence_length > 15) * 1
        
        return formality_score > 0 
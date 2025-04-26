"""
Meme Generator Module

This module is responsible for generating memes based on NLP analysis results.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont
import json
import pkg_resources

class MemeGenerator:
    """Generates memes based on NLP analysis of input text."""
    
    def __init__(self, templates_dir="meme/templates"):
        """
        Initialize the meme generator.
        
        Args:
            templates_dir (str): Directory containing meme templates
        """
        self.templates_dir = templates_dir
        
        # Create templates directory if it doesn't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Load template mappings
        self.template_mappings = self._load_template_mappings()
        
        # Default font for text
        self.default_font_path = self._get_default_font_path()
    
    def _load_template_mappings(self):
        """
        Load mappings between meme templates and NLP characteristics.
        
        Returns:
            dict: Template mappings
        """
        mappings_file = os.path.join(self.templates_dir, "mappings.json")
        
        # If mappings file doesn't exist, create it with default mappings
        if not os.path.exists(mappings_file):
            default_mappings = {
                "sentiment": {
                    "positive": ["happy_drake.jpg", "success_kid.jpg", "expanding_brain.jpg"],
                    "negative": ["sad_cat.jpg", "disappointed_kid.jpg", "this_is_fine.jpg"],
                    "neutral": ["thinking_face.jpg", "unsure_kid.jpg", "idk.jpg"]
                },
                "emotion": {
                    "joy": ["happy_drake.jpg", "success_kid.jpg", "party_parrot.jpg"],
                    "sadness": ["sad_cat.jpg", "disappointed_kid.jpg", "crying_cat.jpg"],
                    "anger": ["angry_cat.jpg", "angry_arthur.jpg", "rage_face.jpg"],
                    "fear": ["scared_cat.jpg", "surprised_pikachu.jpg", "this_is_fine.jpg"],
                    "surprise": ["surprised_pikachu.jpg", "shocked_face.jpg", "mind_blown.jpg"],
                    "disgust": ["disgusted_face.jpg", "eww.jpg", "gross.jpg"],
                    "confusion": ["confused_nick_young.jpg", "unsure_kid.jpg", "thinking_face.jpg"]
                },
                "topic": {
                    "politics": ["thinking_politician.jpg", "policy_drake.jpg", "political_button.jpg"],
                    "technology": ["code_life.jpg", "tech_drake.jpg", "programming.jpg"],
                    "entertainment": ["movie_quote.jpg", "celebrity.jpg", "music.jpg"],
                    "sports": ["sports_win.jpg", "sports_drake.jpg", "team_celebration.jpg"],
                    "business": ["stonks.jpg", "business_cat.jpg", "profit.jpg"],
                    "science": ["science_cat.jpg", "lab_coat.jpg", "experiment.jpg"],
                    "social_media": ["social_drake.jpg", "influencer.jpg", "tweet.jpg"],
                    "memes": ["meta_meme.jpg", "meme_about_memes.jpg", "memeception.jpg"]
                },
                "tone": {
                    "humorous": ["funny_cat.jpg", "laugh_cry.jpg", "comedy.jpg"],
                    "serious_negative": ["serious_cat.jpg", "not_amused.jpg", "disappointed.jpg"],
                    "excited": ["excited_kid.jpg", "celebration.jpg", "party.jpg"],
                    "inquisitive": ["thinking_face.jpg", "question_mark.jpg", "curious.jpg"],
                    "neutral": ["neutral_face.jpg", "ok.jpg", "whatever.jpg"]
                }
            }
            
            # Save default mappings
            os.makedirs(os.path.dirname(mappings_file), exist_ok=True)
            with open(mappings_file, 'w') as f:
                json.dump(default_mappings, f, indent=2)
            
            return default_mappings
        
        # Load existing mappings
        try:
            with open(mappings_file, 'r') as f:
                return json.load(f)
        except:
            # Return empty mappings if loading fails
            return {}
    
    def _get_default_font_path(self):
        """
        Get path to a default font for meme text.
        
        Returns:
            str: Path to default font
        """
        # Try common font locations depending on OS
        possible_fonts = [
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            # macOS
            "/System/Library/Fonts/Supplemental/Impact.ttf",
            "/Library/Fonts/Arial.ttf",
            # Windows
            "C:\\Windows\\Fonts\\impact.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
        ]
        
        for font_path in possible_fonts:
            if os.path.exists(font_path):
                return font_path
        
        # If no system font found, create a fonts directory and prompt user
        fonts_dir = os.path.join(os.path.dirname(self.templates_dir), "fonts")
        os.makedirs(fonts_dir, exist_ok=True)
        
        # Return a placeholder path that will be checked at runtime
        return os.path.join(fonts_dir, "impact.ttf")
    
    def select_template(self, nlp_params):
        """
        Select an appropriate meme template based on NLP analysis.
        
        Args:
            nlp_params (dict): Parameters from NLP analysis
            
        Returns:
            str: Path to selected template image
        """
        # Extract parameters
        sentiment = nlp_params.get("sentiment", "neutral")
        tone = nlp_params.get("tone", "neutral")
        topic = nlp_params.get("topic", "general")
        emotions = nlp_params.get("emotions", [])
        
        candidate_templates = set()
        
        # Add templates matching sentiment
        if sentiment in self.template_mappings.get("sentiment", {}):
            candidate_templates.update(self.template_mappings["sentiment"][sentiment])
        
        # Add templates matching tone
        if tone in self.template_mappings.get("tone", {}):
            candidate_templates.update(self.template_mappings["tone"][tone])
        
        # Add templates matching topic
        if topic in self.template_mappings.get("topic", {}):
            candidate_templates.update(self.template_mappings["topic"][topic])
        
        # Add templates matching emotions (if available)
        for emotion in emotions:
            if emotion in self.template_mappings.get("emotion", {}):
                candidate_templates.update(self.template_mappings["emotion"][emotion])
        
        # If no templates match, use a default set
        if not candidate_templates:
            default_templates = [
                "confused_nick_young.jpg", 
                "thinking_face.jpg", 
                "surprised_pikachu.jpg"
            ]
            template_name = random.choice(default_templates)
        else:
            template_name = random.choice(list(candidate_templates))
        
        # Check if template exists
        template_path = os.path.join(self.templates_dir, template_name)
        if not os.path.exists(template_path):
            # Template doesn't exist, create a placeholder
            self._create_placeholder_template(template_path, template_name)
        
        return template_path
    
    def _create_placeholder_template(self, template_path, template_name):
        """
        Create a placeholder template image if the actual template doesn't exist.
        
        Args:
            template_path (str): Path where the template should be saved
            template_name (str): Name of the template
        """
        # Create a simple image with text
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Try to use the default font, or use a simple font if not available
        try:
            font = ImageFont.truetype(self.default_font_path, 40)
        except:
            font = ImageFont.load_default()
        
        # Draw template name
        draw.text((width // 2, height // 2), f"Placeholder for\n{template_name}", 
                  fill=(0, 0, 0), font=font, anchor="mm", align="center")
        
        # Save image
        os.makedirs(os.path.dirname(template_path), exist_ok=True)
        image.save(template_path)
    
    def generate_caption(self, nlp_params):
        """
        Generate a caption for the meme based on NLP analysis.
        
        Args:
            nlp_params (dict): Parameters from NLP analysis
            
        Returns:
            tuple: (top_text, bottom_text) for the meme
        """
        # Extract the original text
        original_text = nlp_params.get("text", "")
        
        # Simple caption generation - split the text in half
        words = original_text.split()
        
        if len(words) <= 3:
            # Very short text, use as bottom text only
            top_text = ""
            bottom_text = original_text
        else:
            # Split text into top and bottom
            middle = len(words) // 2
            top_text = " ".join(words[:middle])
            bottom_text = " ".join(words[middle:])
        
        return top_text, bottom_text
    
    def create_meme(self, nlp_params, output_path=None):
        """
        Create a meme based on NLP analysis parameters.
        
        Args:
            nlp_params (dict): Parameters from NLP analysis
            output_path (str, optional): Path to save the generated meme
            
        Returns:
            str: Path to the generated meme
        """
        # Select template
        template_path = self.select_template(nlp_params)
        
        # Generate caption
        top_text, bottom_text = self.generate_caption(nlp_params)
        
        # Create output path if not provided
        if output_path is None:
            output_dir = os.path.join(os.path.dirname(self.templates_dir), "output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"meme_{random.randint(1000, 9999)}.jpg")
        
        # Load template image
        try:
            img = Image.open(template_path)
        except:
            # If template can't be loaded, create a blank image
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
        
        # Prepare for drawing
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to use the default font, or use a simple font if not available
        try:
            font_size = width // 10  # Scale font size based on image width
            font = ImageFont.truetype(self.default_font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Helper function to draw text with outline
        def draw_text_with_outline(draw, position, text, font):
            # Draw outline
            outline_color = (0, 0, 0)
            for offset_x, offset_y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                draw.text((position[0] + offset_x, position[1] + offset_y), text, font=font, fill=outline_color, align="center")
            
            # Draw text
            draw.text(position, text, font=font, fill=(255, 255, 255), align="center")
        
        # Draw top text
        if top_text:
            draw_text_with_outline(draw, (width // 2, height // 10), top_text.upper(), font)
        
        # Draw bottom text
        if bottom_text:
            draw_text_with_outline(draw, (width // 2, height - height // 10), bottom_text.upper(), font)
        
        # Save the meme
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        
        return output_path 
import requests
from config import (
    GOOGLE_API_KEY,
    IMAGEFX_API_URL,
    VEO2_API_URL,
    IMAGEFX_CONFIG,
    VEO2_CONFIG
)
import json
from typing import Dict, Any
import logging

class MediaService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_image(self, universe: str, topic: str, style: str = None) -> Dict[str, Any]:
        """
        Generate an image using Image API
        """
        try:
            # Create prompt
            prompt = IMAGEFX_PROMPT_TEMPLATE.format(
                universe=universe,
                topic=topic,
                style=style or "default"
            )

            # Make API request
            headers = {
                'Authorization': f'Bearer {GOOGLE_API_KEY}',
                'Content-Type': 'application/json'
            }

            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": IMAGEFX_CONFIG
            }

            response = requests.post(IMAGE_API_URL, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            image_url = result['candidates'][0]['content']['parts'][0]['text']

            return {
                "success": True,
                "image_url": image_url,
                "style": style or "default",
                "metadata": {
                    "universe": universe,
                    "topic": topic
                }
            }

        except Exception as e:
            self.logger.error(f"Image generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def generate_animation(self, universe: str, topic: str, style: str = None) -> Dict[str, Any]:
        """
        Generate an animation using VEO2 API
        """
        try:
            # Create prompt
            prompt = VEO2_PROMPT_TEMPLATE.format(
                universe=universe,
                topic=topic,
                style=style or "default"
            )

            # Make API request
            headers = {
                'Authorization': f'Bearer {GOOGLE_API_KEY}',
                'Content-Type': 'application/json'
            }

            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": VEO2_CONFIG
            }

            response = requests.post(VEO2_API_URL, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            animation_url = result['candidates'][0]['content']['parts'][0]['text']

            return {
                "success": True,
                "animation_url": animation_url,
                "style": style or "default",
                "metadata": {
                    "universe": universe,
                    "topic": topic
                }
            }

        except Exception as e:
            self.logger.error(f"Animation generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance
media_service = MediaService()

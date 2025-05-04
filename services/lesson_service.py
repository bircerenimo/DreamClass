import requests
import json
import asyncio
from typing import Dict, Any
from config import GOOGLE_API_KEY, GEMINI_API_URL, IMAGE_API_URL
import logging
from concurrent.futures import ThreadPoolExecutor

class LessonService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor()

    def _generate_content(self, prompt: str) -> str:
        """Generate content using Gemini API"""
        headers = {
            'Authorization': f'Bearer {GOOGLE_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "gemini-pro",
            "prompt": {
                "text": prompt
            },
            "temperature": 0.7,
            "candidate_count": 1
        }

        try:
            response = requests.post(GEMINI_API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # JSON yapısını düzelt
            content = result.get('candidates', [{}])[0].get('content', [{}])[0].get('parts', [{}])[0].get('text', '')
            content = content.replace('```json', '').replace('```', '').strip()
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            error_type = type(e).__name__
            error_message = str(e)
            raise Exception({
                'success': False,
                'error': {
                    'type': error_type,
                    'message': error_message
                }
            })

    def _generate_image(self, description: str) -> str:
        """Generate image using Gemini Image API"""
        headers = {
            'Authorization': f'Bearer {GOOGLE_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "contents": [{
                "parts": [{
                    "text": description
                }]
            }]
        }

        try:
            response = requests.post(IMAGE_API_URL, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # JSON yapısını düzelt
            image_url = result.get('candidates', [{}])[0].get('content', [{}])[0].get('parts', [{}])[0].get('text', '')
            return image_url
            
        except Exception as e:
            self.logger.error(f"Image API Error: {str(e)}")
            error_type = type(e).__name__
            error_message = str(e)
            raise Exception({
                'success': False,
                'error': {
                    'type': error_type,
                    'message': error_message
                }
            })

    async def generate_lesson(self, universe: str, topic: str, grade: str) -> Dict[str, Any]:
        """
        Generate a complete lesson plan using Gemini API with caching
        Uses async/await for better performance
        """
        try:
            if not all([universe, topic, grade]):
                raise Exception("Missing required fields")

            # Load prompt template
            with open('data/prompt_template.json', 'r', encoding='utf-8') as f:
                prompt_template = json.load(f)

            # Create prompt using template
            requirements = '\n'.join(prompt_template['requirements']).format(
                topic=topic,
                universe=universe
            )

            prompt = f"""{prompt_template['template'].format(
                topic=topic,
                universe=universe,
                grade=grade
            )}

Requirements:
{requirements}

Return the result as a JSON object with the following structure:
{json.dumps(prompt_template['response_format'], indent=4)}"""

            # Synchronous API çağrılarını yap
            content = self._generate_content(prompt)
            lesson_data = json.loads(content)

            # Görselleri oluştur
            for ve in lesson_data.get("visual_elements", []):
                if ve.get("type") == "image" and "description" in ve:
                    try:
                        image_url = self._generate_image(ve["description"])
                        ve["url"] = image_url
                    except Exception as e:
                        self.logger.error(f"Error generating image: {str(e)}")
                        ve["error"] = str(e)

            response_data = {
                "story": lesson_data.get("story", ""),
                "quiz": lesson_data.get("quiz", []),
                "visual_elements": lesson_data.get("visual_elements", []),
                "metadata": {
                    "universe": universe,
                    "topic": topic,
                    "grade": grade
                },
                "success": True
            }

            self.logger.info(f"Successfully generated lesson for {universe}/{topic}/{grade}")
            return response_data

        except Exception as e:
            self.logger.error(f"Error generating lesson: {str(e)}")
            error_type = type(e).__name__
            error_message = str(e)
            raise Exception({
                "success": False,
                "error": {
                    "type": error_type,
                    "message": error_message
                }
            })

# Create a singleton instance of LessonService
lesson_service = LessonService()

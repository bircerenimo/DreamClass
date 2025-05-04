import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = 'gemini-1.5-flash'

# Error Messages
ERROR_MESSAGES = {
    'INTERNAL_ERROR': 'Internal server error occurred',
    'INVALID_REQUEST': 'Invalid request format',
    'NOT_FOUND': 'Resource not found',
    'DATABASE_ERROR': 'Database connection error',
    'IMAGE_GENERATION_ERROR': 'Image generation failed'
}

# API URLs
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}'
IMAGE_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-vision:generateContent?key={GOOGLE_API_KEY}'
VEO2_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}'
IMAGEFX_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-vision:generateContent?key={GOOGLE_API_KEY}'

# Application Configuration
DEBUG = os.getenv('DEBUG', 'True') == 'True'
PORT = int(os.getenv('PORT', '5000'))
HOST = os.getenv('HOST', '0.0.0.0')

# Prompt Templates
LESSON_PROMPT_TEMPLATE = """Create an engaging lesson about {topic} in the universe of {universe} for grade {grade}.

Requirements:
1. Make it interactive and engaging
2. Include examples and exercises
3. Keep it age-appropriate
4. Use clear and simple language

Return the result as a JSON object with the following structure:
{
    "story": "",
    "quiz": [
        {"question": "", "options": ["", "", "", ""], "answer": ""}
    ],
    "visual_elements": [
        {"type": "image", "description": ""}
    ]
}"""

IMAGEFX_PROMPT_TEMPLATE = """Create an image for a lesson about {topic} in the universe of {universe}.
Style: {style}

Requirements:
1. Make it visually appealing and educational
2. Include relevant elements from the universe
3. Make it suitable for grade level
4. Use bright and engaging colors

Return the image URL."""

VEO2_PROMPT_TEMPLATE = """Create an engaging animation that explains {topic} in {universe} universe.
Style: {style}
Duration: 30-60 seconds
Purpose: Educational explanation
Format: JSON with animation URL and frame descriptions"""

# Response Format
RESPONSE_FORMAT = {
    "universe": "",
    "topic": "",
    "grade": "",
    "story": "",
    "quiz": [],
    "visual_elements": []
}

# Gemini API Configuration
GEMINI_API_CONFIG = {
    "model": "gemini-1.5-flash",
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048
}

# ImageFX Configuration
IMAGEFX_CONFIG = {
    "temperature": 0.7,
    "candidateCount": 1,
    "topK": 40,
    "topP": 0.95
}

# VEO2 Configuration
VEO2_CONFIG = {
    "temperature": 0.7,
    "candidateCount": 1,
    "topK": 40,
    "topP": 0.95
}

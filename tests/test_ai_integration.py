import unittest
import asyncio
from unittest.mock import patch, MagicMock
import os
import sys

# Proje kök dizinini PYTHONPATH'e ekleyelim
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.lesson_service import LessonService
from config import GOOGLE_API_KEY

class TestAIIntegration(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Kontrol etmek için geçici bir API anahtarı kullanalım
        self.temp_api_key = GOOGLE_API_KEY
        self.lesson_service = LessonService()
        
    def tearDown(self):
        # API anahtarını geri alalım
        os.environ['GOOGLE_API_KEY'] = self.temp_api_key

    async def test_ai_integration(self):
        """Yapay zeka entegrasyonunu test et"""
        universe = "Harry Potter"
        topic = "Energy Transformations"
        grade = "6"

        # Test için geçici API anahtarı kullanalım
        os.environ['GOOGLE_API_KEY'] = "test_api_key"

        # Dersi oluştur
        result = await self.lesson_service.generate_lesson(universe, topic, grade)

        # Kontroller
        self.assertIn("story", result)
        self.assertIn("quiz", result)
        self.assertIn("visual_elements", result)
        self.assertTrue(isinstance(result["quiz"], list))
        self.assertTrue(len(result["quiz"]) >= 3)
        self.assertEqual(result["metadata"]["grade"], grade, "Grade mismatch")

    def test_ai_integration_sync(self):
        """Yapay zeka entegrasyonunu test et (sync versiyon)"""
        asyncio.run(self.test_ai_integration())

if __name__ == '__main__':
    unittest.main()

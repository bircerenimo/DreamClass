import unittest
import asyncio
from unittest.mock import patch, MagicMock
import os
import sys

# Proje kök dizinini PYTHONPATH'e ekleyelim
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.lesson_service import LessonService
from config import GOOGLE_API_KEY

class TestLessonService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.lesson_service = LessonService()

    @patch('services.lesson_service.requests')
    async def test_generate_lesson(self, mock_requests):
        """Herhangi bir evren/konu/sınıf için ders oluşturma testi"""
        test_cases = [
            ("Kendi Evrenim", "Matematik", "7"),
            ("Bilim Kurgu Evreni", "Fizik", "9"),
            ("Fantastik Hayvanlar", "Kimya", "12")
        ]
        
        for universe, topic, grade in test_cases:
            # Mock response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'candidates': [{
                    'content': [{
                        'parts': [{
                            'text': '{"story": "Sample story about ' + topic + ' in ' + universe + ' universe", "quiz": [{"question": "Test question about ' + topic + '", "answer": "Test answer"}], "visual_elements": [{"type": "image", "description": "Visual element for ' + topic + '", "purpose": "Educational illustration"}]}'
                        }]
                    }]
                }]
            }
            mock_requests.post.return_value = mock_response
            
            result = await self.lesson_service.generate_lesson(universe, topic, grade)
            self.assertIn("story", result, "Story not found in response")
            self.assertIn("quiz", result, "Quiz not found in response")
            self.assertIn("visual_elements", result, "Visual elements not found in response")
            self.assertEqual(len(result["quiz"]), 1, "Quiz should have one question")
            self.assertEqual(len(result["visual_elements"]), 1, "Should have one visual element")

    def test_generate_lesson_sync(self):
        """Herhangi bir evren/konu/sınıf için ders oluşturma testi (sync versiyon)"""
        asyncio.run(self.test_generate_lesson())

    @patch('services.lesson_service.requests')
    async def test_cache_functionality(self, mock_requests):
        """Önbellekleme testi"""
        universe = "Test Evreni"
        topic = "Test Konusu"
        grade = "10"
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': [{
                    'parts': [{
                        'text': '{"story": "Test story", "quiz": [{"question": "Test question", "answer": "Test answer"}], "visual_elements": [{"type": "image", "description": "Test image", "purpose": "Educational illustration"}]}'
                    }]
                }]
            }]
        }
        mock_requests.post.return_value = mock_response
        
        # İlk kez oluştur
        result1 = await self.lesson_service.generate_lesson(universe, topic, grade)
        
        # İkinci kez aynı istek
        result2 = await self.lesson_service.generate_lesson(universe, topic, grade)
        
        # Önbellekten gelen sonuç aynı olmalı
        self.assertEqual(result1, result2, "Cache not working properly")

    def test_cache_functionality_sync(self):
        """Önbellekleme testi (sync versiyon)"""
        asyncio.run(self.test_cache_functionality())

    @patch('services.lesson_service.requests')
    async def test_error_handling(self, mock_requests):
        """Hata yönetimi testi"""
        universe = "Test Evreni"
        topic = "Test Konusu"
        grade = "10"
        
        # API hatası
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API error")
        mock_requests.post.return_value = mock_response
        
        result = await self.lesson_service.generate_lesson(universe, topic, grade)
        self.assertFalse(result.get("success"), "Should fail on API error")
        self.assertIn("error", result, "Error message not found")

    def test_error_handling_sync(self):
        """Hata yönetimi testi (sync versiyon)"""
        asyncio.run(self.test_error_handling())

    @patch('services.lesson_service.requests')
    async def test_invalid_json_handling(self, mock_requests):
        """Geçersiz JSON formatı testi"""
        universe = "Test Evreni"
        topic = "Test Konusu"
        grade = "10"

        # Geçersiz JSON döndüren mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": [{
                    "parts": [{
                        "text": "Bu geçersiz JSON formatında bir yanıt"
                    }]
                }]
            }]
        }
        mock_requests.post.return_value = mock_response
        
        result = await self.lesson_service.generate_lesson(universe, topic, grade)
        self.assertFalse(result.get("success"), "Should fail on invalid JSON")
        self.assertIn("error", result, "Error message not found")

    def test_invalid_json_handling_sync(self):
        """Geçersiz JSON formatı testi (sync versiyon)"""
        asyncio.run(self.test_invalid_json_handling())

if __name__ == '__main__':
    unittest.main()

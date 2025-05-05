import google.generativeai as genai
import logging
import os
import json
import re
from dotenv import load_dotenv

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def extract_json_from_response(text):
    """
    Cümleler içinden sadece JSON kısmını çıkarır
    """
    try:
        # Metin içindeki ilk { ile son } arasını bul
        match = re.search(r'{.*}', text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)
        else:
            raise ValueError("JSON formatı bulunamadı")
    except Exception as e:
        raise ValueError(f"JSON çıkarma hatası: {str(e)}")

class GeminiAPI:
    def __init__(self):
        try:
            # API anahtarının varlığını kontrol et
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is not set in .env file")
                
            # API anahtarının formatını kontrol et
            if not GOOGLE_API_KEY.startswith('AIza'):
                raise ValueError("Invalid API key format. It should start with 'AIza'")
                
            genai.configure(api_key=GOOGLE_API_KEY)
            logger.info(f"Configured API with key: {GOOGLE_API_KEY[:5]}...{GOOGLE_API_KEY[-5:]}")
            
            # Modeli oluştur
            try:
                # Hikaye oluşturma için model
                self.story_model = genai.GenerativeModel("gemini-1.5-flash")
                # Değerlendirme için model
                self.evaluation_model = genai.GenerativeModel("gemini-1.5-flash")
                logger.info("Created Gemini model instances")
                
                # Modelin çalışıp çalışmadığını test et
                test_prompt = "Test prompt"
                test_response = self.story_model.generate_content(test_prompt)
                logger.info("Test model response successful")
                
                # Prompt şablonlarını yükle
                self.load_prompt_templates()
                
            except Exception as e:
                logger.error(f"Error creating or testing model: {str(e)}")
                raise ValueError(f"Failed to create or test model: {str(e)}")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise ValueError(f"Failed to initialize Gemini API: {str(e)}")
            
    def load_prompt_templates(self):
        """Prompt şablonlarını yükler"""
        try:
            # Hikaye oluşturma şablonu
            with open("data/dynamic_prompt_template.json", "r", encoding="utf-8") as f:
                self.story_template = json.load(f)["prompt_template"]
            logger.info("Loaded story prompt template")
            
            # Değerlendirme şablonu
            with open("data/evaluate_prompt_template.json", "r", encoding="utf-8") as f:
                self.evaluation_template = json.load(f)["prompt_template"]
            logger.info("Loaded evaluation prompt template")
            
        except Exception as e:
            logger.error(f"Error loading prompt templates: {str(e)}")
            raise ValueError(f"Failed to load prompt templates: {str(e)}")

    def generate_story(self, data):
        """
        İlk LLM: Öğrencinin evren, konu ve sınıf seviyesine göre hikaye ve sorular oluşturur
        """
        try:
            # Gerekli verilerin varlığını kontrol et
            required_fields = ['level', 'universe', 'topic']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Prompt şablonunu doldur
            prompt = self.story_template.replace("{{evren}}", data['universe'])\
                                      .replace("{{konu}}", data['topic'])\
                                      .replace("{{seviye}}", data['level'])
            
            logger.info(f"Generating story with prompt: {prompt[:50]}...")
            
            # İçerik üret
            try:
                response = self.story_model.generate_content(prompt)
                logger.info("Successfully generated story content")
            except Exception as e:
                logger.error(f"Error generating story content: {str(e)}")
                raise ValueError(f"Failed to generate story content: {str(e)}")
            
            # Cevabı döndür ve işle
            try:
                if hasattr(response, 'text'):
                    raw_text = response.text
                    logger.info(f"Raw response: {raw_text[:100]}...")
                    
                    # JSON formatına dönüştür
                    parsed_json = extract_json_from_response(raw_text)
                    logger.info(f"Successfully parsed JSON content")
                    
                    # Çıktıyı yapılandır (görsel fikri kaldırıldı)
                    output_data = {
                        "universe": data['universe'],
                        "topic": data['topic'],
                        "level": data['level'],
                        "story": parsed_json.get("story", ""),
                        "quiz": parsed_json.get("quiz", [])
                    }
                    
                    # Çıktıyı JSON dosyasına kaydet (ikinci LLM için bellek olarak)
                    self.save_output_to_file(output_data)
                    
                    return output_data
                else:
                    raise Exception("AI cevabı geçersiz")
            
            except Exception as e:
                logger.error(f"Error processing story response: {str(e)}")
                logger.error(f"Response object: {str(response)}")
                raise ValueError(f"Invalid story response format: {str(e)}")

        except Exception as e:
            logger.error(f"Error in generate_story: {str(e)}")
            raise ValueError(f"Failed to generate story: {str(e)}")
    
    def save_output_to_file(self, output_data):
        """Çıktıyı JSON dosyasına kaydeder (ikinci LLM için bellek)"""
        try:
            with open("data/last_story_output.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            logger.info("Saved story output to file for future reference")
        except Exception as e:
            logger.error(f"Error saving output to file: {str(e)}")
    
    def evaluate_answers(self, answers):
        """
        İkinci LLM: Öğrencinin cevaplarını değerlendirir
        """
        try:
            # Son hikaye çıktısını yükle (ikinci LLM için bellek)
            try:
                with open("data/last_story_output.json", "r", encoding="utf-8") as f:
                    story_data = json.load(f)
                logger.info("Loaded previous story data for evaluation context")
            except Exception as e:
                logger.error(f"Error loading story data: {str(e)}")
                story_data = {"universe": "Bilinmiyor", "topic": "Bilinmiyor", "level": "Bilinmiyor"}
            
            # Soruları ve cevapları birleştir
            sorular_ve_cevaplar = ""
            quiz = story_data.get("quiz", [])
            
            for i, (question, answer) in enumerate(zip(quiz, answers.values()), 1):
                soru_metni = question.get("question", f"Soru {i}")
                sorular_ve_cevaplar += f"Soru {i}: {soru_metni}\nCevabın: {answer}\n\n"
            
            # Değerlendirme şablonunu doldur
            eval_prompt = self.evaluation_template\
                .replace("{{evren}}", story_data.get("universe", "Bilinmiyor"))\
                .replace("{{konu}}", story_data.get("topic", "Bilinmiyor"))\
                .replace("{{seviye}}", story_data.get("level", "Bilinmiyor"))\
                .replace("{{sorular_ve_cevaplar}}", sorular_ve_cevaplar)
            
            logger.info(f"Evaluating answers with prompt: {eval_prompt[:100]}...")
            
            # Değerlendirme yap
            try:
                response = self.evaluation_model.generate_content(eval_prompt)
                logger.info("Successfully generated evaluation")
            except Exception as e:
                logger.error(f"Error generating evaluation: {str(e)}")
                raise ValueError(f"Failed to generate evaluation: {str(e)}")
            
            # Değerlendirme sonucunu döndür
            if hasattr(response, 'text'):
                evaluation_text = response.text
                logger.info(f"Evaluation response: {evaluation_text[:100]}...")
                return evaluation_text
            else:
                raise Exception("AI değerlendirme cevabı geçersiz")
                
        except Exception as e:
            logger.error(f"Error in evaluate_answers: {str(e)}")
            raise ValueError(f"Failed to evaluate answers: {str(e)}")
    
    def generate_content(self, data):
        """
        Geriye dönük uyumluluk için eski fonksiyonu koruyoruz
        """
        return self.generate_story(data)


if __name__ == '__main__':
    api = GeminiAPI()
    
    # Test hikaye oluşturma
    test_data = {
        'universe': 'Minecraft',
        'topic': 'Enerji dönüşümü',
        'level': '6'
    }
    
    try:
        # Hikaye oluştur
        story_result = api.generate_story(test_data)
        print("\n🧠 Hikaye Sonucu:\n")
        print(json.dumps(story_result, indent=4, ensure_ascii=False))
        
        # Test cevapları değerlendir
        test_answers = {
            'cevap1': 'Demir cevherini eritmek için.',
            'cevap2': 'Isı enerjisi barındırır. Su ile temas edince obsidyen oluşur.',
            'cevap3': 'Kimyasal enerji ışık enerjisine dönüşür.'
        }
        
        evaluation_result = api.evaluate_answers(test_answers)
        print("\n📊 Değerlendirme Sonucu:\n")
        print(evaluation_result)
        
    except Exception as e:
        print("Error:", str(e))

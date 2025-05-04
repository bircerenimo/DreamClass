from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from services.gemini_api import GeminiAPI
import logging
from flask_cors import CORS
import urllib.parse

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Test modu için sabit yanıt
TEST_MODE = False  # Production modunda çalışıyoruz, AI'den gerçek yanıt alacağız

gemini_api = GeminiAPI()

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        # Gelen veriyi al
        data = request.get_json()
        logger.info(f"Received request data: {data}")
        
        # Gerekli alanları kontrol et
        required_fields = ['universe', 'topic', 'level']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': True,
                'message': 'Missing required fields: universe, topic, level'
            }), 400

        # Gemini API'ye doğru formatta veri gönder
        try:
            # Gerekli verileri doğrula
            if not all(field in data for field in ['universe', 'topic', 'level']):
                return jsonify({
                    'error': True,
                    'message': 'Missing required fields: universe, topic, level'
                }), 400

            # API'ye doğru formatta veri gönder
            response = gemini_api.generate_content(data)
            
            # Response'u kontrol et
            if not response:
                return jsonify({
                    'error': True,
                    'message': 'No response from API'
                }), 500

            # Response'u döndür
            return jsonify({
                'error': False,
                'message': 'Content generated successfully',
                'content': response
            })

        except Exception as e:
            logger.error(f"Error in API call: {str(e)}")
            return jsonify({
                'error': True,
                'message': f'Error generating content: {str(e)}'
            }), 500
        
        # Yanıtın JSON formatında olup olmadığını kontrol et
        try:
            data = response.json()
        except ValueError:
            # JSON değilse düz metni döndür
            return jsonify({
                'error': False,
                'message': 'Content generated successfully',
                'content': response.text
            })

        # Yanıtta hata varsa hata mesajı döndür
        if 'error' in data:
            return jsonify({
                'error': True,
                'message': data['message']
            }), 500

        # Yanıtın JSON formatında olduğunu varsayarak parse et
        try:
            parsed = data['content']
            return jsonify({
                'error': False,
                'message': 'Content generated successfully',
                'content': {
                    'story': parsed['story'],
                    'quiz': parsed['quiz'],
                    'visualIdea': parsed['visualIdea']
                }
            })
        except (KeyError, TypeError):
            # JSON formatında değilse veya beklenmeyen bir format varsa düz metni döndür
            return jsonify({
                'error': False,
                'message': 'Content generated successfully',
                'content': data['content']
            })

    except Exception as e:
        logger.error(f"Error in generate_content: {str(e)}")
        return jsonify({
            'error': True,
            'message': f'Error generating content: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=os.getenv('DEBUG', 'False').lower() == 'true', port=port)

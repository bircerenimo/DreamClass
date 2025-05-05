from flask import Flask, jsonify, request, render_template, send_from_directory
import os
from config import HOST, PORT, DEBUG
from api.generate import api
from services.lesson_service import lesson_service

app = Flask(__name__, template_folder=os.path.abspath('templates'))
app.config['JSON_AS_ASCII'] = False  # Türkçe karakter desteği için
app.register_blueprint(api)

@app.route('/')
def hello():
    return render_template('test.html')

@app.route('/api')
def api_info():
    return 'DreamClass Backend API is running!'

@app.route('/api/generate', methods=['POST'])
async def generate():
    try:
        data = request.json
        
        # Gerekli alanları kontrol et
        if not all(key in data for key in ['universe', 'topic', 'grade']):
            return jsonify({
                'success': False,
                'error': {
                    'type': 'ValidationError',
                    'message': 'Missing required fields: universe, topic, grade'
                }
            }), 400
            
        universe = data['universe']
        topic = data['topic']
        grade = data['grade']
        
        # Dersi oluştur
        result = await lesson_service.generate_lesson(universe, topic, grade)
        
        story = result['story']
        quiz = result['quiz']
        visual_elements = result['visual_elements']
        
        response = {
            "universe": universe,
            "topic": topic,
            "grade": grade,
            "story": story,
            "quiz": quiz,
            "visual_elements": visual_elements,
            "success": True
        }
        
        # Başarılı yanıt
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'type': 'InternalServerError',
                'message': str(e)
            }
        }), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

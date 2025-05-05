from flask import Blueprint, request, jsonify
from services.lesson_service import lesson_service
from services.media_service import media_service
from services.gemini_api import GeminiAPI
from config import DEBUG

api = Blueprint('api', __name__)

# Gemini API instance
gemini_api = GeminiAPI()

@api.route('/api/generate', methods=['POST'])
def generate_lesson():
    try:
        # Get input data
        data = request.json
        
        # Extract parameters
        universe = data.get('universe')
        topic = data.get('topic')
        level = data.get('level')  # Changed from 'grade' to 'level' to match frontend
        
        # Validate required fields
        if not all([universe, topic, level]):
            return jsonify({"error": "Universe, topic, and level are required"}), 400
        
        # Generate story and quiz using Gemini API directly
        try:
            story_data = {
                'universe': universe,
                'topic': topic,
                'level': level
            }
            
            result = gemini_api.generate_story(story_data)
            
            # Format response
            response = {
                "story": result.get("story", ""),
                "quiz": result.get("quiz", []),
                "metadata": {
                    "universe": universe,
                    "topic": topic,
                    "level": level
                },
                "success": True
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({"error": f"Error generating content: {str(e)}"}), 500
        
    except Exception as e:
        if DEBUG:
            return jsonify({"error": str(e)}), 500
        return jsonify({"error": "An error occurred while generating the lesson"}), 500

@api.route('/api/evaluate', methods=['POST'])
def evaluate_answers():
    try:
        # Get student answers
        answers = request.json
        
        # Validate input
        if not answers or not isinstance(answers, dict):
            return jsonify({"error": "Invalid answers format"}), 400
        
        # Evaluate answers using Gemini API
        try:
            evaluation_result = gemini_api.evaluate_answers(answers)
            
            # Return evaluation result
            return jsonify({
                "evaluation": evaluation_result,
                "success": True
            })
            
        except Exception as e:
            return jsonify({"error": f"Error evaluating answers: {str(e)}"}), 500
        
    except Exception as e:
        if DEBUG:
            return jsonify({"error": str(e)}), 500
        return jsonify({"error": "An error occurred while evaluating the answers"}), 500

@api.route('/api/generate/image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        universe = data.get('universe')
        topic = data.get('topic')
        style = data.get('style')
        
        if not universe or not topic:
            return jsonify({"error": "Universe and topic are required"}), 400
        
        result = media_service.generate_image(universe, topic, style)
        return jsonify(result)
        
    except Exception as e:
        if DEBUG:
            return jsonify({"error": str(e)}), 500
        return jsonify({"error": "An error occurred while generating the image"}), 500

@api.route('/api/generate/animation', methods=['POST'])
def generate_animation():
    try:
        data = request.json
        universe = data.get('universe')
        topic = data.get('topic')
        style = data.get('style')
        
        if not universe or not topic:
            return jsonify({"error": "Universe and topic are required"}), 400
        
        result = media_service.generate_animation(universe, topic, style)
        return jsonify(result)
        
    except Exception as e:
        if DEBUG:
            return jsonify({"error": str(e)}), 500
        return jsonify({"error": "An error occurred while generating the animation"}), 500

# Register error handlers
@api.errorhandler(400)
def handle_bad_request(e):
    return jsonify({
        "error": "Bad Request",
        "message": str(e)
    }), 400

@api.errorhandler(500)
def handle_server_error(e):
    return jsonify({
        "error": "Internal Server Error",
        "message": str(e) if DEBUG else "An unexpected error occurred"
    }), 500

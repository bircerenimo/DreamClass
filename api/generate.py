from flask import Blueprint, request, jsonify
from services.lesson_service import lesson_service
from services.media_service import media_service
from config import DEBUG

api = Blueprint('api', __name__)

@api.route('/api/generate', methods=['POST'])
def generate_lesson():
    try:
        # Get input data
        data = request.json
        
        # Extract parameters
        universe = data.get('universe')
        topic = data.get('topic')
        grade = data.get('grade')
        
        # Generate lesson content
        result = lesson_service.generate_lesson(universe, topic, grade)
        
        # Format response
        response = {
            "story": result.get("story", ""),
            "quiz": result.get("quiz", []),
            "visual_elements": result.get("visual_elements", []),
            "dream_power_score": result.get("dream_power_score", 0),
            "metadata": {
                "universe": universe,
                "topic": topic,
                "grade": grade
            },
            "success": result.get("success", False)
        }
        
        return jsonify(response)
        
    except Exception as e:
        if DEBUG:
            return jsonify({"error": str(e)}), 500
        return jsonify({"error": "An error occurred while generating the lesson"}), 500

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

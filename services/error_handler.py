from typing import Dict, Any, Optional
from datetime import datetime
import json
import logging
from config import ERROR_MESSAGES
from flask import jsonify

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error):
        status_code = 500
        error_type = 'INTERNAL_ERROR'
        
        if isinstance(error, KeyError):
            error_type = 'INVALID_REQUEST'
            status_code = 400
        elif isinstance(error, ValueError):
            error_type = 'INVALID_REQUEST'
            status_code = 400
        elif isinstance(error, Exception):
            error_type = 'INTERNAL_ERROR'
            status_code = 500

        self.logger.error(f"Error occurred: {error_type} - {str(error)}")
        return jsonify({
            'error': True,
            'message': ERROR_MESSAGES.get(error_type, 'Unknown error occurred'),
            'details': str(error)
        }), status_code

    def format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format successful response data
        """
        return {
            "success": True,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

    def format_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Format error response
        """
        error_type = type(error).__name__
        error_message = str(error)
        timestamp = datetime.now().isoformat()
        
        # Get error message from config if available
        error_code = error_type.lower()
        custom_message = ERROR_MESSAGES.get(error_code, error_message)
        
        error_response = {
            "success": False,
            "error": {
                "type": error_type,
                "code": error_code,
                "message": custom_message,
                "timestamp": timestamp
            }
        }
        
        # Add context if provided
        if context:
            error_response["error"]["context"] = context
            
        self.logger.error(f"Error: {error_type} - {error_message}")
        if context:
            self.logger.error(f"Context: {context}")
            
        return error_response

        # Log error details
        error_details = {
            "type": error_type,
            "message": error_message,
            "timestamp": timestamp,
            "context": context or {}
        }
        self.logger.error(f"API Error: {json.dumps(error_details)}")

        # Format error response
        error_data = {
            "error": {
                "type": error_type,
                "message": "An error occurred while processing your request",
                "timestamp": timestamp,
                "details": error_details if context else None
            },
            "success": False
        }

        return error_data

    def format_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Format error into a standardized response
        """
        error_type = type(error).__name__
        error_message = str(error)
        timestamp = datetime.now().isoformat()

        # Log error details
        error_details = {
            "type": error_type,
            "message": error_message,
            "timestamp": timestamp
        }

        if context:
            error_details["context"] = context

        self.logger.error(f"Error occurred: {error_details}")

        # Return standardized error response
        return {
            "success": False,
            "error": {
                "type": error_type,
                "message": error_message,
                "timestamp": timestamp
            }
        }

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate API response structure
        Returns False with error log if validation fails
        """
        required_fields = ["story", "quiz", "visual_elements", "success"]
        missing_fields = [field for field in required_fields if field not in response]

        if missing_fields:
            self.logger.error(f"Invalid response format: Missing fields {missing_fields}")
            return False

        # Additional validation
        if not isinstance(response.get("quiz"), list):
            self.logger.error("Invalid quiz format: Must be a list")
            return False

        if not isinstance(response.get("visual_elements"), list):
            self.logger.error("Invalid visual_elements format: Must be a list")
            return False

        return True

    def format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format successful API response
        Adds metadata and validates data
        """
        try:
            # Validate data format
            if not self.validate_response(data):
                raise ValueError("Invalid response format")

            # Format response
            response = {
                "data": data,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "request_id": self._generate_request_id()
                },
                "success": True
            }

            self.logger.info(f"Successful response: {response['metadata']['request_id']}")
            return response

        except Exception as e:
            self.logger.error(f"Error formatting response: {str(e)}")
            return self.handle_error(e)

    def _generate_request_id(self) -> str:
        """Generate unique request ID for tracking"""
        import random
        return f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"

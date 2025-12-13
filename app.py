"""
Password Generator Flask Application
Enhanced with cryptographic security, input validation, error handling, and rate limiting
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_limiter import Limiter  # pyright: ignore[reportMissingImports]
from flask_limiter.util import get_remote_address  # pyright: ignore[reportMissingImports]
import os
import logging
import logic  # Import shared logic

# ========== LOGGING CONFIGURATION - START ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# ========== LOGGING CONFIGURATION - END ==========

# ========== CUSTOM EXCEPTION CLASSES - START ==========
class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass
# ========== CUSTOM EXCEPTION CLASSES - END ==========

app = Flask(__name__, static_folder=".", static_url_path="")

# ========== RATE LIMITING CONFIGURATION - START ==========
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)
logger.info("Rate limiter initialized: 100 requests per minute per IP")
# ========== RATE LIMITING CONFIGURATION - END ==========


# ========== VALIDATION FUNCTIONS - START ==========
def validate_password_params(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    """
    Validate parameters for password generation.
    """
    # Validate length
    if not isinstance(length, int):
        raise ValidationError("Length must be an integer")
    
    if length < 4 or length > 128:
        raise ValidationError("Length must be between 4 and 128 characters")
    
    # Validate that at least one character type is selected
    if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
        raise ValidationError("At least one character type must be selected")
    
    logger.info(f"Password params validated: length={length}")


def validate_passphrase_params(word_count, separator, capitalize):
    """
    Validate parameters for passphrase generation.
    """
    # Validate word count
    if not isinstance(word_count, int):
        raise ValidationError("Word count must be an integer")
    
    if word_count < 2 or word_count > 20:
        raise ValidationError("Word count must be between 2 and 20")
    
    # Validate separator (allow any string, but warn if too long)
    if not isinstance(separator, str):
        raise ValidationError("Separator must be a string")
    
    if len(separator) > 10:
        raise ValidationError("Separator must be 10 characters or less")
    
    # Validate capitalize mode
    valid_modes = ['title', 'lower', 'upper']
    if capitalize not in valid_modes:
        raise ValidationError(f"Capitalize must be one of: {', '.join(valid_modes)}")
    
    logger.info(f"Passphrase params validated: word_count={word_count}, capitalize={capitalize}")
# ========== VALIDATION FUNCTIONS - END ==========


@app.route("/")
def serve_index():
    """Serve the main index.html page"""
    try:
        return send_from_directory(app.static_folder, "index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({"error": "Failed to load page"}), 500


@app.route("/api/config", methods=["GET"])
def get_config():
    """
    Return configuration data, including the word list.
    This allows the frontend to have the same word list as the backend.
    """
    return jsonify({
        "wordList": logic.get_word_list()
    })


@app.route("/api/generate-password", methods=["POST"])
@limiter.limit("100 per minute")
def generate_password():
    """
    Generate a random password with specified parameters.
    """
    try:
        # Get JSON data
        data = request.get_json(force=True) or {}
        
        # Extract and convert parameters
        length = int(data.get("length", 12))
        use_uppercase = bool(data.get("useUppercase", True))
        use_lowercase = bool(data.get("useLowercase", True))
        use_numbers = bool(data.get("useNumbers", True))
        use_symbols = bool(data.get("useSymbols", True))
        exclude_ambiguous = bool(data.get("excludeAmbiguous", False))
        
        # Validate parameters
        validate_password_params(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
        
        # Generate password using shared logic
        password = logic.generate_password(
            length=length,
            use_uppercase=use_uppercase,
            use_lowercase=use_lowercase,
            use_numbers=use_numbers,
            use_symbols=use_symbols,
            exclude_ambiguous=exclude_ambiguous
        )
        
        logger.info(f"Password generated successfully: length={length}")
        return jsonify({"password": password})
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except logic.GenerationError as e:
        logger.error(f"Generation error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        logger.warning(f"Invalid input type: {str(e)}")
        return jsonify({"error": "Invalid parameter type"}), 400
    except Exception as e:
        logger.error(f"Unexpected error in generate_password: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/generate-passphrase", methods=["POST"])
@limiter.limit("100 per minute")
def generate_passphrase():
    """
    Generate a passphrase using random words from the word list.
    """
    try:
        # Get JSON data
        data = request.get_json(force=True) or {}
        
        # Extract and convert parameters with defaults
        word_count = int(data.get("wordCount", 4))
        separator = str(data.get("separator", "-"))
        add_numbers = bool(data.get("addNumbers", True))
        add_symbols = bool(data.get("addSymbols", True))
        capitalize_mode = str(data.get("capitalize", "title"))
        
        # Validate parameters
        validate_passphrase_params(word_count, separator, capitalize_mode)
        
        # Generate passphrase using shared logic
        passphrase = logic.generate_passphrase(
            word_count=word_count,
            separator=separator,
            add_numbers=add_numbers,
            add_symbols=add_symbols,
            capitalize_mode=capitalize_mode
        )
        
        logger.info(f"Passphrase generated successfully: word_count={word_count}")
        return jsonify({"passphrase": passphrase})
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        logger.warning(f"Invalid input type: {str(e)}")
        return jsonify({"error": "Invalid parameter type"}), 400
    except Exception as e:
        logger.error(f"Unexpected error in generate_passphrase: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# ========== ERROR HANDLERS - START ==========
@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors"""
    logger.warning(f"Rate limit exceeded: {get_remote_address()}")
    return jsonify({
        "error": "Rate limit exceeded. Please wait before making more requests.",
        "retry_after": e.description
    }), 429


@app.errorhandler(404)
def not_found_handler(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500
# ========== ERROR HANDLERS - END ==========


if __name__ == "__main__":
    # Default to 5001 to avoid conflict with Apple AirPlay on macOS
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("DEBUG", "True").lower() == "true"
    
    logger.info(f"🚀 Starting Password Generator on http://localhost:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("Security: Using cryptographically secure random number generator")
    logger.info("Rate limiting: 100 requests per minute per IP")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
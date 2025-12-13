"""
Password Generator Flask Application
Enhanced with cryptographic security, input validation, error handling, and rate limiting
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_limiter import Limiter  # pyright: ignore[reportMissingImports]
from flask_limiter.util import get_remote_address  # pyright: ignore[reportMissingImports]
import secrets  # Cryptographically secure random number generator
import string
import os
import logging

# ========== LOGGING CONFIGURATION - START ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# ========== LOGGING CONFIGURATION - END ==========

# ========== WORD LIST FOR PASSPHRASE GENERATION - START ==========
WORD_LIST = [
    # Animals
    'cat', 'dog', 'lion', 'tiger', 'bear', 'wolf', 'eagle', 'shark', 'dragon', 'phoenix',
    'rabbit', 'horse', 'elephant', 'dolphin', 'penguin', 'falcon', 'panther', 'leopard',
    'cheetah', 'rhino', 'zebra', 'giraffe', 'monkey', 'gorilla', 'whale', 'octopus',
    
    # Colors
    'red', 'blue', 'green', 'purple', 'orange', 'silver', 'gold', 'crimson', 'azure',
    'emerald', 'violet', 'amber', 'coral', 'ivory', 'jade', 'ruby', 'topaz', 'onyx',
    
    # Nature
    'ocean', 'mountain', 'forest', 'river', 'cloud', 'storm', 'thunder', 'sunset',
    'rainbow', 'garden', 'meadow', 'valley', 'canyon', 'desert', 'glacier', 'volcano',
    'spring', 'summer', 'autumn', 'winter', 'breeze', 'wind', 'rain', 'snow',
    
    # Objects
    'table', 'chair', 'laptop', 'phone', 'camera', 'robot', 'rocket', 'castle',
    'bridge', 'tower', 'diamond', 'crystal', 'mirror', 'lamp', 'clock', 'compass',
    'anchor', 'shield', 'sword', 'arrow', 'crown', 'throne', 'wagon', 'ship',
    
    # Actions/Verbs
    'jump', 'run', 'dance', 'swim', 'fly', 'create', 'build', 'dream', 'think',
    'laugh', 'smile', 'sing', 'write', 'paint', 'climb', 'explore', 'discover',
    
    # Adjectives
    'quick', 'brave', 'wise', 'happy', 'strong', 'bright', 'swift', 'bold',
    'calm', 'fierce', 'gentle', 'mighty', 'noble', 'royal', 'silent', 'wild',
    
    # Food
    'pizza', 'coffee', 'apple', 'bread', 'honey', 'berry', 'mango', 'lemon',
    'cherry', 'peach', 'grape', 'melon', 'banana', 'coconut',
    
    # Tech/Modern
    'cyber', 'digital', 'quantum', 'neural', 'binary', 'data', 'pixel', 'byte',
    'code', 'network', 'signal', 'pulse', 'matrix', 'nexus', 'core',
    
    # Abstract/Misc
    'magic', 'shadow', 'light', 'star', 'moon', 'sun', 'time', 'space', 'future',
    'power', 'energy', 'spirit', 'soul', 'cosmos', 'zenith', 'echo', 'mystic',
    'legend', 'myth', 'hero', 'quest', 'journey', 'destiny', 'fortune', 'glory',
    
    # Places
    'city', 'town', 'village', 'island', 'temple', 'palace', 'fortress', 'harbor',
    'square', 'avenue', 'street', 'plaza', 'market', 'academy', 'library', 'arena',
    
    # Elements
    'fire', 'water', 'earth', 'metal', 'stone', 'wood', 'ice', 'flame', 'frost',
    'spark', 'blaze', 'steam', 'smoke', 'mist', 'fog', 'dew', 'ash',
    
    # Celestial
    'comet', 'meteor', 'planet', 'galaxy', 'nebula', 'stellar', 'lunar',
    'solar', 'astral', 'orbit', 'eclipse', 'aurora', 'nova',
    
    # Emotions/States
    'joy', 'peace', 'hope', 'faith', 'truth', 'trust', 'courage', 'honor',
    'grace', 'charm', 'valor', 'pride', 'victory', 'triumph'
]
# ========== WORD LIST FOR PASSPHRASE GENERATION - END ==========

# ========== CUSTOM EXCEPTION CLASSES - START ==========
class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class GenerationError(Exception):
    """Custom exception for password generation errors"""
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
    
    Args:
        length: Password length
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_numbers: Include numbers
        use_symbols: Include symbols
    
    Raises:
        ValidationError: If parameters are invalid
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
    
    Args:
        word_count: Number of words
        separator: Word separator
        capitalize: Capitalization mode
    
    Raises:
        ValidationError: If parameters are invalid
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


def build_character_pool(use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_ambiguous):
    """
    Build a character pool for password generation.
    
    Args:
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_numbers: Include numbers
        use_symbols: Include symbols
        exclude_ambiguous: Exclude ambiguous characters
    
    Returns:
        String containing all allowed characters
    """
    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if exclude_ambiguous:
        for ch in "0Ol1I":
            characters = characters.replace(ch, "")

    return characters


def apply_capitalization(words, capitalize_mode):
    """
    Apply capitalization to a list of words.
    
    Args:
        words: List of words to capitalize
        capitalize_mode: 'title', 'lower', or 'upper'
    
    Returns:
        List of capitalized words
    """
    if capitalize_mode == 'title':
        return [word.capitalize() for word in words]
    elif capitalize_mode == 'upper':
        return [word.upper() for word in words]
    else:  # 'lower' or default
        return [word.lower() for word in words]


@app.route("/")
def serve_index():
    """Serve the main index.html page"""
    try:
        return send_from_directory(app.static_folder, "index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({"error": "Failed to load page"}), 500


@app.route("/api/generate-password", methods=["POST"])
@limiter.limit("100 per minute")
def generate_password():
    """
    Generate a random password with specified parameters.
    
    Request JSON:
    {
        "length": 16,
        "useUppercase": true,
        "useLowercase": true,
        "useNumbers": true,
        "useSymbols": true,
        "excludeAmbiguous": false
    }
    
    Returns:
    {
        "password": "X7k#mP2@qR9zL4wN"
    }
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
        
        # Build character pool
        characters = build_character_pool(
            use_uppercase,
            use_lowercase,
            use_numbers,
            use_symbols,
            exclude_ambiguous,
        )
        
        if not characters:
            raise GenerationError("No characters available for password generation")
        
        # Generate password using cryptographically secure random
        password = "".join(secrets.choice(characters) for _ in range(length))
        
        logger.info(f"Password generated successfully: length={length}")
        return jsonify({"password": password})
        
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except GenerationError as e:
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
    
    Request JSON:
    {
        "wordCount": 4,
        "separator": "-",
        "addNumbers": true,
        "addSymbols": true,
        "capitalize": "title"
    }
    
    Returns:
    {
        "passphrase": "Purple-Dragon-Mountain-89!"
    }
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
        
        # Clamp word count to safe range (3-6 for API, but we validate 2-20)
        word_count = max(3, min(6, word_count))
        
        # Select random words using cryptographically secure random
        # Using secrets.SystemRandom().sample for secure random sampling
        secure_random = secrets.SystemRandom()
        selected_words = secure_random.sample(WORD_LIST, word_count)
        
        # Apply capitalization
        selected_words = apply_capitalization(selected_words, capitalize_mode)
        
        # Join words with separator
        passphrase = separator.join(selected_words)
        
        # Add numbers if requested (using secrets for randomness)
        if add_numbers:
            number = secure_random.randint(1, 99)
            passphrase += str(number)
        
        # Add symbol if requested (using secrets for randomness)
        if add_symbols:
            symbols = "!@#$%"
            symbol = secrets.choice(symbols)
            passphrase += symbol
        
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
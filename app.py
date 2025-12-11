from flask import Flask, jsonify, request, send_from_directory  # pyright: ignore[reportMissingImports]
import random
import string
import os

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

app = Flask(__name__, static_folder=".", static_url_path="")


def build_character_pool(use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_ambiguous):
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


# ========== PASSPHRASE HELPER FUNCTION - START ==========
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
# ========== PASSPHRASE HELPER FUNCTION - END ==========


@app.route("/")
def serve_index():
    # Serve index.html from the same directory
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/generate-password", methods=["POST"])
def generate_password():
    data = request.get_json(force=True) or {}
    length = int(data.get("length", 12))
    use_uppercase = bool(data.get("useUppercase", True))
    use_lowercase = bool(data.get("useLowercase", True))
    use_numbers = bool(data.get("useNumbers", True))
    use_symbols = bool(data.get("useSymbols", True))
    exclude_ambiguous = bool(data.get("excludeAmbiguous", False))

    characters = build_character_pool(
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols,
        exclude_ambiguous,
    )

    if not characters:
        return jsonify({"error": "No character sets selected"}), 400

    password = "".join(random.choice(characters) for _ in range(length))
    return jsonify({"password": password})


# ========== NEW PASSPHRASE ENDPOINT - START ==========
@app.route("/api/generate-passphrase", methods=["POST"])
def generate_passphrase():
    """
    Generate a passphrase using random words from the word list.
    
    Request JSON format:
    {
        "wordCount": 4,              # 3-6 words
        "separator": "-",            # "-", "_", " ", or ""
        "addNumbers": true,          # Add 1-2 digit number
        "addSymbols": true,          # Add symbol at end
        "capitalize": "title"        # "title", "lower", or "upper"
    }
    
    Returns:
    {
        "passphrase": "Purple-Dragon-Mountain-89!"
    }
    """
    data = request.get_json(force=True) or {}
    
    # Get parameters with defaults
    word_count = int(data.get("wordCount", 4))
    separator = data.get("separator", "-")
    add_numbers = bool(data.get("addNumbers", True))
    add_symbols = bool(data.get("addSymbols", True))
    capitalize_mode = data.get("capitalize", "title")
    
    # Validate word count (3-6 words)
    word_count = max(3, min(6, word_count))
    
    # Select random words (ensure no duplicates)
    selected_words = random.sample(WORD_LIST, word_count)
    
    # Apply capitalization
    selected_words = apply_capitalization(selected_words, capitalize_mode)
    
    # Join words with separator
    passphrase = separator.join(selected_words)
    
    # Add numbers if requested
    if add_numbers:
        number = random.randint(1, 99)
        passphrase += str(number)
    
    # Add symbol if requested
    if add_symbols:
        symbols = "!@#$%"
        symbol = random.choice(symbols)
        passphrase += symbol
    
    return jsonify({"passphrase": passphrase})
# ========== NEW PASSPHRASE ENDPOINT - END ==========


if __name__ == "__main__":
    # Default to 5001 to avoid conflict with Apple AirPlay on macOS
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 Starting Password Generator on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)


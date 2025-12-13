"""
Core logic for Password Generator.
Handles secure random generation and shared data methods.
"""

import secrets
import string
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== WORD LIST ==========
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

# ========== EXCEPTIONS ==========
class GenerationError(Exception):
    """Custom exception for password generation errors"""
    pass

# ========== LOGIC FUNCTIONS ==========

def build_character_pool(use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True, exclude_ambiguous=False):
    """
    Build a character pool for password generation.
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

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True, exclude_ambiguous=False):
    """
    Generate a secure random password.
    """
    characters = build_character_pool(use_uppercase, use_lowercase, use_numbers, use_symbols, exclude_ambiguous)
    
    if not characters:
        raise GenerationError("No characters available for password generation. Please select at least one character type.")
    
    # Generate password using cryptographically secure random
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password

def apply_capitalization(words, capitalize_mode):
    """
    Apply capitalization to a list of words.
    """
    if capitalize_mode == 'title':
        return [word.capitalize() for word in words]
    elif capitalize_mode == 'upper':
        return [word.upper() for word in words]
    else:  # 'lower' or default
        return [word.lower() for word in words]

def generate_passphrase(word_count=4, separator="-", add_numbers=True, add_symbols=True, capitalize_mode="title"):
    """
    Generate a secure random passphrase.
    """
    # Clamp word count
    word_count = max(2, min(20, word_count))
    
    # Secure sampling
    secure_random = secrets.SystemRandom()
    selected_words = secure_random.sample(WORD_LIST, word_count)
    
    # Capitalization
    selected_words = apply_capitalization(selected_words, capitalize_mode)
    
    # Join
    passphrase = separator.join(selected_words)
    
    # Add number
    if add_numbers:
        number = secure_random.randint(1, 99)
        passphrase += str(number)
    
    # Add symbol
    if add_symbols:
        symbols = "!@#$%"
        symbol = secrets.choice(symbols)
        passphrase += symbol
        
    return passphrase

def calculate_strength(password):
    """
    Evaluates password strength based on multiple criteria.
    Returns a tuple: (strength_score, strength_text, color_code)
    Note: color_code is ANSI for terminal use.
    """
    strength = 0
    
    # Award points for length
    if len(password) >= 16:
        strength += 3
    elif len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
    
    # Award points for character variety
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 2
    
    # Determine overall strength level
    if strength <= 3:
        return (strength, "Weak", "\033[91m")  # Red
    elif strength <= 5:
        return (strength, "Medium", "\033[93m")  # Yellow
    elif strength <= 7:
        return (strength, "Strong", "\033[92m")  # Green
    else:
        return (strength, "Very Strong", "\033[92m")  # Green

def get_word_list():
    return WORD_LIST

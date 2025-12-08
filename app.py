from flask import Flask, jsonify, request, send_from_directory
import random
import string
import os

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


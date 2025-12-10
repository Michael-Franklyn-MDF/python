# 🔐 Password Generator

A modern, secure, and feature-rich password generator with a beautiful web interface and Flask backend.

![Password Generator Demo](https://img.shields.io/badge/Status-Active-success)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)

## ✨ Features

### 🎯 Core Functionality
- **Secure Password Generation**: Create strong, cryptographically random passwords
- **Customizable Options**:
  - Adjustable length (8-32 characters)
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special symbols (!@#$%^&*)
  - Exclude ambiguous characters (0, O, l, 1, I)

### 📜 Password History
- **Automatic Saving**: Every generated password is stored locally
- **10-Item Limit**: Keeps your most recent 10 passwords
- **Individual Controls**:
  - 📋 **Copy**: One-click copy any previous password
  - 🗑️ **Delete**: Remove individual passwords
  - 🧹 **Clear All**: Bulk delete with confirmation
- **Rich Metadata**:
  - Timestamp (e.g., "2 mins ago")
  - Password length
  - Strength indicator (🔴 Weak, 🟡 Medium, 🟢 Strong)
- **Persistent Storage**: History survives browser refresh using localStorage

### 🌙 Theme Support
- **Light Mode**: Clean, elegant cream theme (default)
- **Dark Mode**: Eye-friendly dark theme
- **Persistent Preference**: Your choice is remembered
- **Smooth Transitions**: Animated theme switching
- **One-Click Toggle**: Easy access button in top-right corner

### 💪 Password Strength Analysis
- **Real-time Evaluation**: Instant feedback as you configure
- **Visual Indicators**: Color-coded strength bar and emoji
- **Smart Scoring**: Based on length and character variety

### 🎨 User Interface
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile
- **Modern Aesthetics**: Elegant typography and smooth animations
- **Intuitive Controls**: Clear labels and helpful placeholders
- **Accessibility**: Semantic HTML and ARIA labels

### 🔌 RESTful API
- **JSON Endpoint**: `/api/generate-password` for programmatic access
- **Easy Integration**: Use in scripts, tools, or other applications
- **Error Handling**: Clear error messages for invalid requests

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone or download** this repository:
```bash
cd /path/to/your/project
```

2. **Create a virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
python -m pip install --upgrade pip
python -m pip install flask
```

### Running the Application

**Default Port (5000):**
```bash
python app.py
```

**Custom Port:**
```bash
PORT=8080 python app.py
```

Then open your browser to: `http://localhost:5000` (or your chosen port)

## 📖 Usage Guide

### Web Interface

1. **Adjust Settings**:
   - Use the slider to set password length
   - Check/uncheck character type options
   - Optionally exclude ambiguous characters

2. **Generate Password**:
   - Click "Generate Password" button
   - Or press Enter key

3. **Copy Password**:
   - Click "📋 Copy" button next to password
   - Or copy from history items

4. **Toggle Theme**:
   - Click 🌙/☀️ button in top-right corner

5. **Manage History**:
   - View all generated passwords below
   - Copy any previous password
   - Delete individual items or clear all

### API Usage

**Endpoint:** `POST /api/generate-password`

**Request Body:**
```json
{
  "length": 16,
  "useUppercase": true,
  "useLowercase": true,
  "useNumbers": true,
  "useSymbols": true,
  "excludeAmbiguous": false
}
```

**Success Response (200):**
```json
{
  "password": "X7k#mP2@qR9zL4wN"
}
```

**Error Response (400):**
```json
{
  "error": "No character sets selected"
}
```

**Example with cURL:**
```bash
curl -X POST http://localhost:5000/api/generate-password \
  -H "Content-Type: application/json" \
  -d '{
    "length": 20,
    "useUppercase": true,
    "useLowercase": true,
    "useNumbers": true,
    "useSymbols": true,
    "excludeAmbiguous": false
  }'
```

**Example with Python:**
```python
import requests

response = requests.post('http://localhost:5000/api/generate-password', json={
    'length': 16,
    'useUppercase': True,
    'useLowercase': True,
    'useNumbers': True,
    'useSymbols': True,
    'excludeAmbiguous': False
})

password = response.json()['password']
print(f"Generated: {password}")
```

## 📁 Project Structure

```
password-generator/
├── app.py              # Flask backend server
├── index.html          # Main HTML structure
├── style.css           # Styles and theme definitions
├── script.js           # Frontend logic and interactivity
├── project.py          # CLI version (standalone)
├── lesson.py           # Python learning exercises
├── README.md           # This file
└── .venv/              # Virtual environment (not in git)
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Vanilla JavaScript (no frameworks)
- **Styling**: Pure CSS with CSS Variables
- **Storage**: Browser localStorage API
- **Security**: Python's `random` and `string` modules

## 🔒 Security Notes

- Passwords are generated using Python's `random.choice()` for sufficient randomness
- History is stored **only in your browser** (localStorage) - never sent to server
- No passwords are logged or stored server-side
- All data stays on your device
- For production use, consider using `secrets` module instead of `random`

## 🎓 Learning Features

This project demonstrates:
- **SDLC Methodology**: Proper planning, design, implementation, and testing
- **Separation of Concerns**: Distinct HTML, CSS, and JavaScript files
- **RESTful API Design**: Clean endpoint structure
- **State Management**: localStorage for persistence
- **Responsive Design**: Mobile-first CSS approach
- **User Experience**: Smooth animations and clear feedback
- **Error Handling**: Graceful degradation and user-friendly messages

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
PORT=5001 python app.py
```

### localStorage Not Working
- Check if cookies/localStorage are enabled in browser
- Try opening in incognito/private mode to test
- Some browsers block localStorage for `file://` URLs

### Pip Cache Permissions Warning
```bash
# Fix permissions (macOS/Linux)
sudo chown -R "$(whoami)" ~/Library/Caches/pip

# Or simply ignore - it's just a warning
```

### Theme Not Saving
- Clear browser cache and reload
- Check browser console (F12) for errors
- Ensure JavaScript is enabled

## 📝 Development Notes

### SDLC Process Used
This project followed the Software Development Life Cycle:
1. **Planning**: Defined features (Password History, Dark Mode)
2. **Analysis**: Identified technical requirements and risks
3. **Design**: Created UI mockups and system architecture
4. **Implementation**: Built features incrementally with testing
5. **Testing**: Verified functionality across scenarios
6. **Deployment**: Documented setup and usage
7. **Maintenance**: Ongoing improvements and bug fixes

### Future Enhancement Ideas
- [ ] Passphrase generator (word-based passwords)
- [ ] Batch password generation
- [ ] Export history to file
- [ ] Password strength checker for existing passwords
- [ ] Browser extension version
- [ ] Multiple theme options
- [ ] QR code generation for WiFi sharing
- [ ] Integration with password managers

## 🤝 Contributing

This is a learning project, but suggestions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a Python learning project to practice:
- Web development fundamentals
- Flask backend development
- JavaScript DOM manipulation
- CSS styling and theming
- Software development lifecycle (SDLC)

## 🙏 Acknowledgments

- Built with guidance on proper SDLC methodology
- Inspired by modern password manager interfaces
- Emoji icons from Unicode standard

---

**⭐ If this project helped you learn, consider starring it!**

**Need help?** Open an issue or check the troubleshooting section above.

# 🚀 Password Generator - Setup Guide

Complete installation and setup instructions for the enhanced Password Generator application with security improvements and new features.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Running Tests](#running-tests)
6. [New Features](#new-features)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.9 or higher**
  - Check version: `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

- **pip** (Python package installer)
  - Usually comes with Python
  - Check version: `pip --version`

### Recommended Tools

- **Virtual Environment** (venv)
  - Built into Python 3.3+
  
- **Git** (for version control)
  - Download: [git-scm.com](https://git-scm.com/)

---

## Installation Steps

### Step 1: Clone or Download the Repository

```bash
# If using Git
git clone <repository-url>
cd password-generator

# Or download and extract the ZIP file
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt when activated.

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

This will install:
- **Flask 3.0+** - Web framework
- **Flask-Limiter 3.5+** - Rate limiting
- **pytest 7.4+** - Testing framework
- **pytest-flask 1.3+** - Flask testing utilities
- **pytest-cov 4.1+** - Code coverage
- **pyperclip 1.8+** - Clipboard functionality (optional)

### Step 5: Verify Installation

```bash
# Check installed packages
pip list

# Should see Flask, Flask-Limiter, pytest, etc.
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```bash
# Server Configuration
PORT=5001
HOST=0.0.0.0
DEBUG=True

# Rate Limiting
RATELIMIT_ENABLED=True
RATELIMIT_DEFAULT=100 per minute

# Password Constraints
PASSWORD_MIN_LENGTH=4
PASSWORD_MAX_LENGTH=128

# Passphrase Constraints
PASSPHRASE_MIN_WORDS=2
PASSPHRASE_MAX_WORDS=20

# Logging
LOG_LEVEL=INFO
```

### Configuration File

The application uses `config.py` for centralized configuration. You can modify settings there or use environment variables to override them.

**Available Configurations:**
- `development` - Default, debug mode enabled
- `production` - Debug disabled, optimized for production
- `testing` - For running tests

Set environment: `export FLASK_ENV=production`

---

## Running the Application

### Standard Run

```bash
# Using default port (5001)
python app.py
```

### Custom Port

```bash
# Using environment variable
PORT=8080 python app.py

# Or export it first
export PORT=8080
python app.py
```

### Production Mode

```bash
# Disable debug mode for production
FLASK_ENV=production DEBUG=False python app.py
```

### Access the Application

Open your browser to:
- Local: `http://localhost:5001`
- Network: `http://<your-ip>:5001`

---

## Running Tests

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v

# Or use the test file directly
python tests/test_app.py
```

### Run with Coverage Report

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Tests

```bash
# Run only password generation tests
pytest tests/test_app.py::test_generate_password_success -v

# Run only validation tests
pytest tests/test_app.py -k "validation" -v

# Run security tests
pytest tests/test_app.py -k "security" -v
```

### Test Coverage Goals

- **Target**: >80% code coverage
- **Current Features Tested**:
  - ✅ Password generation (all character types)
  - ✅ Passphrase generation (all options)
  - ✅ Input validation
  - ✅ API endpoints
  - ✅ Error handling
  - ✅ Randomness/security
  - ✅ Rate limiting

---

## New Features

### 🔒 Security Enhancements

#### 1. Cryptographically Secure Random Generation

**What Changed:**
- Replaced `random.choice()` with `secrets.choice()`
- Replaced `random.sample()` with `secrets.SystemRandom().sample()`
- Replaced `random.randint()` with `secrets.SystemRandom().randint()`

**Why It Matters:**
- `secrets` module uses OS-level cryptographic random number generation
- More secure for password generation
- Suitable for security-sensitive applications

**Testing:**
```python
# Old way (less secure)
password = ''.join(random.choice(chars) for _ in range(length))

# New way (cryptographically secure)
password = ''.join(secrets.choice(chars) for _ in range(length))
```

#### 2. Input Validation

**What's Validated:**
- Password length: 4-128 characters
- At least one character type selected
- Word count: 2-20 words (3-6 for API)
- Separator length: max 10 characters
- Capitalization mode: title/lower/upper only

**Error Messages:**
```json
{
  "error": "Length must be between 4 and 128 characters"
}
```

#### 3. Rate Limiting

**Configuration:**
- **Default**: 100 requests per minute per IP
- **Response when exceeded**: HTTP 429
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

**Test Rate Limiting:**
```bash
# Send 101 requests quickly
for i in {1..101}; do
  curl -X POST http://localhost:5001/api/generate-password \
    -H "Content-Type: application/json" \
    -d '{"length": 16, "useUppercase": true, "useLowercase": true, "useNumbers": true, "useSymbols": true}'
done
```

The 101st request should return:
```json
{
  "error": "Rate limit exceeded. Please wait before making more requests.",
  "retry_after": "60 seconds"
}
```

#### 4. Error Handling

**New Error Types:**
- `ValidationError` - Invalid input parameters
- `GenerationError` - Password generation failures
- `429 Rate Limit Exceeded` - Too many requests
- `404 Not Found` - Invalid endpoint
- `500 Internal Server Error` - Server errors

**All errors return JSON:**
```json
{
  "error": "Description of what went wrong"
}
```

#### 5. Logging

**What's Logged:**
- Server startup information
- Successful password/passphrase generations
- Validation errors
- Rate limit violations
- Internal errors

**View Logs:**
```bash
# Logs appear in console when running
python app.py

# Example output:
# 2024-12-13 10:30:45 - app - INFO - Password generated successfully: length=16
# 2024-12-13 10:30:50 - app - WARNING - Rate limit exceeded: 192.168.1.100
```

### 📦 New Files

1. **`requirements.txt`** - All Python dependencies with versions
2. **`tests/test_app.py`** - Comprehensive unit tests
3. **`config.py`** - Centralized configuration
4. **`SETUP_GUIDE.md`** - This file!

---

## Troubleshooting

### Issue: Port Already in Use

```bash
# Error: Address already in use
# Solution: Use a different port
PORT=8080 python app.py

# Or find and kill the process using port 5001
# macOS/Linux:
lsof -ti:5001 | xargs kill -9

# Windows:
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Issue: ModuleNotFoundError

```bash
# Error: No module named 'flask' or 'flask_limiter'
# Solution: Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: Rate Limiting Not Working

```bash
# Check if Flask-Limiter is installed
pip show Flask-Limiter

# Verify it's enabled in config
python -c "from config import Config; print(Config.RATELIMIT_ENABLED)"
```

### Issue: Tests Failing

```bash
# Make sure you're in the project root directory
cd /path/to/password-generator

# Ensure virtual environment is activated
source .venv/bin/activate

# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests with verbose output
pytest -v

# If specific tests fail, run them individually
pytest tests/test_app.py::test_generate_password_success -v
```

### Issue: Import Errors in Tests

```bash
# Error: cannot import name 'app' from 'app'
# Solution: Make sure you're running from project root
cd /path/to/password-generator
pytest -v

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest -v
```

### Issue: Coverage Report Not Generated

```bash
# Make sure pytest-cov is installed
pip install pytest-cov

# Generate coverage report
pytest --cov=app --cov-report=html --cov-report=term

# If htmlcov folder doesn't appear
pytest --cov=app --cov-report=html:htmlcov
```

---

## Next Steps

### 📚 Learn More

- Read the main [README.md](README.md) for features and usage
- Check the [SDLC To-Do List](TODO.md) for upcoming features
- Review [API Documentation](#) for endpoint details

### 🎯 What's Next?

The following features are planned (see SDLC to-do list):

**Medium Priority Features:**
- ✅ Security hardening (COMPLETED)
- ⏳ Batch password generation (10+ at once)
- ⏳ Password requirements presets (Website, Email, Banking, WiFi)
- ⏳ Keyboard shortcuts (Ctrl+G to generate, etc.)
- ⏳ Export history functionality

### 🤝 Contributing

Want to help? Check out these good first issues:
- Add more unit tests (aim for >90% coverage)
- Implement keyboard shortcuts
- Add batch generation feature
- Create password strength checker for existing passwords

---

## 📊 Project Status

### Completed ✅

- ✅ Cryptographically secure random generation
- ✅ Input validation and error handling
- ✅ Rate limiting (100 req/min)
- ✅ Unit tests with >80% coverage
- ✅ Comprehensive logging
- ✅ Configuration file
- ✅ requirements.txt

### In Progress ⏳

- ⏳ Batch generation feature
- ⏳ Password presets
- ⏳ Keyboard shortcuts

### Planned 📋

- 📋 Export history to file
- 📋 Strength checker for existing passwords
- 📋 Custom word lists

---

## 📞 Support

### Getting Help

1. **Read the Documentation**
   - [README.md](README.md) - Features and basic usage
   - [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation (this file)
   - [SDLC To-Do List](TODO.md) - Development roadmap

2. **Check Troubleshooting Section**
   - See above for common issues

3. **Run Tests**
   - Tests can help identify configuration issues
   - `pytest -v` for detailed output

4. **Check Logs**
   - Server logs show detailed error information
   - Look for ERROR and WARNING messages

---

## 🎉 Success!

If you see this message in your terminal, you're all set:

```
🚀 Starting Password Generator on http://localhost:5001
Debug mode: True
Security: Using cryptographically secure random number generator
Rate limiting: 100 requests per minute per IP
 * Running on http://0.0.0.0:5001
```

**You're ready to generate secure passwords!** 🔐

Visit `http://localhost:5001` in your browser and start generating passwords.

---

**Last Updated:** December 13, 2024  
**Version:** 2.0.0 (Security Enhanced)
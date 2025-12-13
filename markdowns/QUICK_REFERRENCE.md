# 🚀 Quick Reference - Command Cheat Sheet

Essential commands for working with the enhanced Password Generator.

---

## 📦 Setup Commands

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\activate              # Windows

# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

## 🏃 Running the Application

```bash
# Standard run (port 5001)
python app.py

# Custom port
PORT=8080 python app.py

# Production mode
FLASK_ENV=production DEBUG=False python app.py

# With environment variables
DEBUG=False LOG_LEVEL=WARNING PORT=8000 python app.py
```

---

## 🧪 Testing Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app

# Run with HTML coverage report
pytest --cov=app --cov-report=html

# Run with coverage and open report
pytest --cov=app --cov-report=html && open htmlcov/index.html

# Run specific test
pytest tests/test_app.py::test_generate_password_success -v

# Run tests matching pattern
pytest -k "password" -v
pytest -k "validation" -v
pytest -k "security" -v

# Run tests with output
pytest -v -s

# Stop on first failure
pytest -x
```

---

## 📊 Coverage Commands

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Generate terminal coverage report
pytest --cov=app --cov-report=term

# Generate both HTML and terminal
pytest --cov=app --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html              # macOS
xdg-open htmlcov/index.html          # Linux
start htmlcov/index.html             # Windows

# Check coverage percentage
pytest --cov=app --cov-report=term-missing
```

---

## 🔍 Debugging Commands

```bash
# Check which process is using port
lsof -i :5001                        # macOS/Linux
netstat -ano | findstr :5001         # Windows

# Kill process on port
lsof -ti:5001 | xargs kill -9        # macOS/Linux
taskkill /F /PID <PID>               # Windows

# View Python version
python --version
python3 --version

# View pip version
pip --version

# List installed packages
pip list
pip freeze

# Check specific package
pip show Flask
pip show Flask-Limiter
```

---

## 🌐 API Testing Commands

### Using cURL

```bash
# Test password generation
curl -X POST http://localhost:5001/api/generate-password \
  -H "Content-Type: application/json" \
  -d '{
    "length": 16,
    "useUppercase": true,
    "useLowercase": true,
    "useNumbers": true,
    "useSymbols": true,
    "excludeAmbiguous": false
  }'

# Test passphrase generation
curl -X POST http://localhost:5001/api/generate-passphrase \
  -H "Content-Type: application/json" \
  -d '{
    "wordCount": 4,
    "separator": "-",
    "addNumbers": true,
    "addSymbols": true,
    "capitalize": "title"
  }'

# Test rate limiting (send 101 requests)
for i in {1..101}; do
  curl -X POST http://localhost:5001/api/generate-password \
    -H "Content-Type: application/json" \
    -d '{"length": 16, "useUppercase": true, "useLowercase": true, "useNumbers": true, "useSymbols": true}'
  echo ""
done

# Test validation error
curl -X POST http://localhost:5001/api/generate-password \
  -H "Content-Type: application/json" \
  -d '{
    "length": 200,
    "useUppercase": true,
    "useLowercase": true,
    "useNumbers": true,
    "useSymbols": true
  }'
```

### Using Python

```bash
# Interactive Python testing
python3

>>> import requests
>>> 
>>> # Generate password
>>> r = requests.post('http://localhost:5001/api/generate-password', json={
...     'length': 16,
...     'useUppercase': True,
...     'useLowercase': True,
...     'useNumbers': True,
...     'useSymbols': True
... })
>>> print(r.json())
>>> 
>>> # Generate passphrase
>>> r = requests.post('http://localhost:5001/api/generate-passphrase', json={
...     'wordCount': 4,
...     'separator': '-',
...     'addNumbers': True,
...     'addSymbols': True,
...     'capitalize': 'title'
... })
>>> print(r.json())
```

---

## 📝 Git Commands

```bash
# Check status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Add security enhancements: secrets module, validation, rate limiting"

# Push to remote
git push origin main

# Create new branch
git checkout -b feature/batch-generation

# View commit history
git log --oneline

# View changes
git diff

# Undo changes (before commit)
git checkout -- app.py
```

---

## 🔧 Environment Variables

```bash
# Set environment variables (macOS/Linux)
export PORT=8080
export DEBUG=False
export RATELIMIT_DEFAULT="50 per minute"

# Set environment variables (Windows)
set PORT=8080
set DEBUG=False

# Use .env file (if using python-dotenv)
echo "PORT=8080" > .env
echo "DEBUG=False" >> .env
echo "RATELIMIT_DEFAULT=50 per minute" >> .env

# Run with inline environment variables
PORT=8080 DEBUG=False python app.py
```

---

## 🧹 Cleanup Commands

```bash
# Remove __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove .pytest_cache
rm -rf .pytest_cache

# Remove coverage files
rm -rf htmlcov .coverage

# Remove all generated files
rm -rf __pycache__ .pytest_cache htmlcov .coverage *.pyc

# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf .venv
```

---

## 📦 Package Management

```bash
# Install specific package
pip install flask==3.0.0

# Install with specific version
pip install "Flask>=3.0.0"

# Uninstall package
pip uninstall flask

# Update package
pip install --upgrade flask

# Install from requirements.txt
pip install -r requirements.txt

# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Install in development mode
pip install -e .
```

---

## 🔒 Security Checks

```bash
# Check for security vulnerabilities
pip install safety
safety check

# Check for outdated packages
pip list --outdated

# Update all packages (use with caution)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
```

---

## 📊 Performance Testing

```bash
# Install Apache Bench
# macOS: brew install ab
# Ubuntu: sudo apt-get install apache2-utils

# Performance test
ab -n 1000 -c 10 -p payload.json -T application/json http://localhost:5001/api/generate-password

# Create payload.json first:
echo '{"length": 16, "useUppercase": true, "useLowercase": true, "useNumbers": true, "useSymbols": true}' > payload.json
```

---

## 🎯 Common Workflows

### Fresh Install
```bash
git clone <repo-url>
cd password-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Development Workflow
```bash
source .venv/bin/activate
python app.py
# Make changes...
pytest -v
git add .
git commit -m "Description"
git push
```

### Testing Workflow
```bash
source .venv/bin/activate
pytest -v --cov=app
# Fix failing tests...
pytest -v --cov=app --cov-report=html
open htmlcov/index.html
```

### Deployment Preparation
```bash
# Update requirements
pip freeze > requirements.txt

# Run all tests
pytest -v

# Check coverage
pytest --cov=app --cov-report=term

# Run in production mode
FLASK_ENV=production DEBUG=False python app.py
```

---

## 🆘 Troubleshooting Commands

```bash
# Check Python installation
which python3
python3 --version

# Check pip installation
which pip
pip --version

# Check virtual environment
echo $VIRTUAL_ENV                    # macOS/Linux
echo %VIRTUAL_ENV%                   # Windows

# Verify Flask installation
python -c "import flask; print(flask.__version__)"

# Verify Flask-Limiter installation
python -c "import flask_limiter; print(flask_limiter.__version__)"

# Check if port is available
nc -zv localhost 5001                # macOS/Linux
Test-NetConnection -ComputerName localhost -Port 5001  # Windows PowerShell

# View Flask app routes
python -c "from app import app; print(app.url_map)"
```

---

## 💡 Pro Tips

```bash
# Create alias for common commands (add to ~/.bashrc or ~/.zshrc)
alias venv="source .venv/bin/activate"
alias runapp="python app.py"
alias testapp="pytest -v --cov=app"

# Use after sourcing .bashrc/.zshrc:
venv && runapp
venv && testapp

# Watch mode for tests (requires pytest-watch)
pip install pytest-watch
ptw -- -v

# Run app with auto-reload (Flask debug mode)
FLASK_DEBUG=1 python app.py

# Quick test specific function
pytest tests/test_app.py::test_generate_password_success -v -s
```

---

## 📚 Documentation Commands

```bash
# Generate API documentation (if using Sphinx)
pip install sphinx
sphinx-quickstart
make html

# View README
cat README.md
less README.md

# View specific documentation
cat SETUP_GUIDE.md
cat ENHANCEMENT_SUMMARY.md
cat QUICK_REFERENCE.md
```

---

## 🎉 One-Liner Shortcuts

```bash
# Full setup in one line
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# Test and coverage report
pytest -v --cov=app --cov-report=html && open htmlcov/index.html

# Clean and test
rm -rf __pycache__ .pytest_cache htmlcov .coverage && pytest -v

# Update dependencies
pip list --outdated && pip freeze > requirements.txt

# Full deployment check
pytest -v && FLASK_ENV=production DEBUG=False python app.py
```

---

**💡 Tip:** Bookmark this page for quick access to all commands!

**Last Updated:** December 13, 2024
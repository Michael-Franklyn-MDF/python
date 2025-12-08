# Password Generator (Web + Flask API)

A simple password generator with a Flask backend (`app.py`) and a web UI (`index.html` + `script.js` + `style.css`).

## Prerequisites
- Python 3.9+ (comes with `python3` on macOS)
- Pip

## Setup
```bash
cd /Users/franklyn/Desktop/Intro
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
```

## Run
```bash
# default port 5000; choose another if 5000 is busy
python app.py
# or override the port, e.g.:
# PORT=5001 python app.py
```

Open the app at `http://localhost:5000` (or your chosen port).

## API
`POST /api/generate-password`
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
Response:
```json
{ "password": "..." }
```

Returns `400` if no character sets are selected.

## Notes
- Frontend calls the API; no separate build step required.
- If `pip` cache permissions warn, you can ignore or `sudo chown -R "$(whoami)" ~/Library/Caches/pip`.


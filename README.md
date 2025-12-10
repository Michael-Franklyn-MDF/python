# Password Generator (Web + Flask API)

A secure, convenient, and modern password generator featuring:
- Flask backend (`app.py`)
- Responsive web UI (`index.html`, `script.js`, `style.css`)
- Password history and light/dark mode

## Features

- **Secure Password Generation:** Customize length, character sets, and exclude ambiguous characters.
- **Web User Interface:** Clean design for desktop and mobile, with theme switching (light/dark mode).
- **Password History:** Every password generated is saved in a session-based history list for future use.
  - Each history entry features:
    - **Copy:** Instantly copy any previous password.
    - **Delete:** Remove individual previous passwords from the list.
    - **Clear All:** Quickly clear your password history.
- **RESTful API:** `/api/generate-password` endpoint for integration with other tools.

## Prerequisites

- Python 3.9+
- pip

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
```

## Running the App

```bash
# default port 5000; choose another if 5000 is busy
python app.py
# or override the port, e.g.:
# PORT=5001 python app.py
```

Open the app at `http://localhost:5000` (or your chosen port).

## API Reference

**POST** `/api/generate-password`

Request body:
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
*Returns `400` if no character sets are selected.*

## Recent Updates

- **Password History:** Generated passwords are saved for the session. You can:
  - Copy any saved password
  - Delete individual passwords from the history
  - Clear all passwords from the history at once
- **Theme Support:** Toggle between light and dark mode at any time.
- Improved instructions and onboarding in the README.
- Enhanced API usage guidance for developers.

## Notes

- The frontend interacts directly with the backend API. No build step is required.
- If you see pip cache permission warnings, they can usually be ignored. Alternatively, run:  
  `sudo chown -R "$(whoami)" ~/Library/Caches/pip`

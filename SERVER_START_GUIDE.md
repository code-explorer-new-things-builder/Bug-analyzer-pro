# Server Startup Guide

## Quick Start Command

```bash
C:\Users\pattn\AppData\Local\Programs\Python\Python312\python.exe app.py
```

## Why This Command Works

- **Full Python Path**: Windows has Python path issues with aliases. Using the full path to Python312 ensures the correct interpreter is used.
- **Location**: `C:\Users\pattn\AppData\Local\Programs\Python\Python312\python.exe` is where Python 3.12 is installed with all dependencies.
- **App File**: `app.py` is the Flask application in the project root.

## What Happens When Started

1. Loads environment variables from `.env` file
2. Initializes Gemini 2.5 Flash AI service
3. Starts Flask development server
4. Server runs on `http://localhost:5000`

## Expected Output

```
2026-02-13 22:04:27 - src.ai.ai_service - INFO - Gemini AI service initialized successfully
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.29.239:5000
```

## Access Points

- **Local**: http://localhost:5000
- **Network**: http://192.168.29.239:5000

## Troubleshooting

### If Python Not Found
- Don't use `python` or `python3` - they trigger Windows app aliases
- Always use the full path: `C:\Users\pattn\AppData\Local\Programs\Python\Python312\python.exe`

### If Dependencies Missing
- Run: `pip install -r requirements.txt`
- Use the same Python path if needed

### If Port 5000 Already in Use
- Change PORT in `.env` file
- Or kill the process using port 5000

## Environment Variables (.env)

```
GEMINI_API_KEY
FLASK_ENV=development
PORT=5000
```

These are automatically loaded when the app starts.

## To Stop the Server

Press `CTRL+C` in the terminal where the server is running.

---

**Last Updated**: February 13, 2026
**Python Version**: 3.12
**Framework**: Flask 3.1.1


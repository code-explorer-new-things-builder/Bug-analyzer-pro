# Web Application Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key

Get your free API key from: https://makersuite.google.com/app/apikey

Create a `.env` file in the project root with:
```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
PORT=5000
```

The application will automatically load these environment variables when it starts.

### 3. Run the Web Application

```bash
python app.py
```

The application will start on: **http://localhost:5000**

## Features

### ✨ AI-Enhanced Analysis (Gemini 2.5 Flash)
- Fast, efficient flash model for real-time analysis
- Toggle AI enhancement on/off
- Get context-aware explanations
- Receive specific fix suggestions
- Learn best practices

### 🔍 Code Analysis
- **Bug Detection**: Infinite loops, unreachable code, null pointers
- **Multi-Language**: Python, JavaScript, Java
- **Real-time**: Instant analysis results
- **Quality Metrics**: Code quality score and issue breakdown

### 🎨 Beautiful UI
- Modern, responsive design
- Color-coded severity levels
- Code syntax highlighting
- Easy-to-read results

## API Endpoints

### POST /api/analyze
Analyze code and detect issues.

**Request:**
```json
{
  "code": "def test():\n    while True:\n        pass",
  "language": "python",
  "use_ai": true
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "findings": [...],
    "metrics": {...}
  },
  "ai_enabled": true
}
```

### POST /api/ai-analysis
Get AI analysis of code.

**Request:**
```json
{
  "code": "your code here",
  "language": "python"
}
```

### GET /api/health
Check service health and AI availability.

## Usage Examples

### Example 1: Python Code with Bug
```python
def process_data():
    while True:
        print("Processing...")
    return "Done"  # Unreachable
```

**Result**: Detects infinite loop (CRITICAL) and unreachable code (MEDIUM)

### Example 2: JavaScript with Issues
```javascript
function calculate(x) {
    if (x > 0) {
        return x * 2;
        console.log("Done");  // Unreachable
    }
}
```

**Result**: Detects unreachable code after return

### Example 3: Clean Code
```python
def add(a, b):
    """Add two numbers."""
    if a is None or b is None:
        return 0
    return a + b
```

**Result**: ✅ No issues found!

## Troubleshooting

### AI Not Working?
- Check if GEMINI_API_KEY is set correctly
- Verify API key is valid at https://makersuite.google.com
- Check console for error messages

### Port Already in Use?
Change the port:
```bash
PORT=8000 python app.py
```

### Dependencies Missing?
```bash
pip install --upgrade -r requirements.txt
```

## For Hackathon Demo

1. **Start the server**: `python app.py`
2. **Open browser**: http://localhost:5000
3. **Paste sample code** with bugs
4. **Enable AI enhancement**
5. **Click "Analyze Code"**
6. **Show results** with AI explanations!

## Demo Script

1. **Introduction**: "This is an AI-powered code review assistant"
2. **Show UI**: Clean, modern interface
3. **Paste buggy code**: Use the infinite loop example
4. **Analyze without AI**: Show basic detection
5. **Enable AI**: Toggle AI enhancement
6. **Analyze with AI**: Show enhanced explanations
7. **Highlight features**: 
   - Multi-language support
   - Real-time analysis
   - Quality metrics
   - AI-powered insights

## Next Steps

- Add more bug detection rules
- Implement security scanning
- Add style checking
- Create user accounts
- Save analysis history
- Export reports (PDF, JSON)

---

**Built with ❤️ for the hackathon**

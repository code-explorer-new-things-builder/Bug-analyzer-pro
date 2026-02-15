# AI-Powered Code Review Assistant

An intelligent code review tool that helps developers write better, more secure code through educational feedback and AI-enhanced analysis.

## Features

- 🔍 Multi-language support (Python, JavaScript, Java)
- 🐛 Bug detection with detailed explanations
- 🔒 Security vulnerability scanning
- 📝 Code style and best practice checking
- 🤖 Optional AI enhancement for context-aware analysis
- 📚 Educational feedback with examples and resources
- 📊 Comprehensive quality metrics and reports

## Project Structure

```
.
├── src/                    # Source code
│   ├── models/            # Data models
│   ├── parsers/           # Language parsers
│   ├── config/            # Configuration management
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── config/                # Configuration files
├── docs/                  # Documentation
└── .kiro/specs/          # Project specifications
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Web Application (Recommended for Hackathon Demo)

```bash
# Install dependencies
pip install -r requirements.txt

# Set Gemini API key
set GEMINI_API_KEY=your_api_key_here

# Run web app
python app.py
```

Open http://localhost:5000 in your browser!

See [WEB_APP_GUIDE.md](WEB_APP_GUIDE.md) for detailed instructions.

### Command Line (Coming Soon)

```bash
# Analyze a single file
python -m src.cli analyze mycode.py

# Analyze with AI enhancement
python -m src.cli analyze mycode.py --use-ai
```

## Configuration

Create a `.reviewrc.json` file in your project root:

```json
{
  "enabled_checks": ["bug", "security", "style"],
  "severity_threshold": "low",
  "use_ai": false,
  "output_format": "markdown"
}
```

## Development Status

- ✅ Language Parser (Python, JavaScript, Java)
- ✅ Core Data Models
- ✅ Configuration Management
- ✅ Logging Infrastructure
- 🚧 Bug Detector (In Progress)
- 🚧 Security Scanner (Planned)
- 🚧 Style Checker (Planned)
- 🚧 AI Integration (Planned)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## License

MIT License

## Contributing

Contributions are welcome! Please read our contributing guidelines first.

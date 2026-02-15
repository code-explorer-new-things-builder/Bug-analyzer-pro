# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-code-review-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
pytest tests/
```

## Configuration

Create a `.reviewrc.json` file in your project root or home directory:

```json
{
  "enabled_checks": ["bug", "security", "style"],
  "severity_threshold": "low",
  "use_ai": false,
  "output_format": "markdown"
}
```

## Directory Structure

```
.
├── src/                    # Source code
│   ├── models/            # Data models (Finding, AnalysisResult, Config)
│   ├── parsers/           # Language parsers (Python, JS, Java)
│   ├── config/            # Configuration management
│   └── utils/             # Utilities (logging, helpers)
├── tests/                 # Unit tests
├── config/                # Default configurations
└── docs/                  # Documentation
```

## Next Steps

- See [USAGE.md](USAGE.md) for usage examples
- See [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines

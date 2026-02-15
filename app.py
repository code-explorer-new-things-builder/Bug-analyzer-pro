"""Flask web application for AI Code Review Assistant."""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.parsers import LanguageParser, PythonParser, JavaScriptParser, JavaParser
from src.analyzers import BugDetector
from src.ai import AIService
from src.models import AnalysisResult, QualityMetrics

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
parser = LanguageParser()
parser.register_parser('python', PythonParser())
parser.register_parser('javascript', JavaScriptParser())
parser.register_parser('java', JavaParser())

bug_detector = BugDetector()
ai_service = AIService()


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """Analyze code endpoint."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        use_ai = data.get('use_ai', False)
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Parse code
        parse_result = parser.parse(code, language)
        
        if not parse_result.success:
            return jsonify({
                'success': False,
                'error': parse_result.error_message
            }), 400
        
        # Detect bugs
        findings = bug_detector.detect_bugs(parse_result.ast, code, language)
        
        # AI enhancement if enabled
        if use_ai and ai_service.is_available():
            for finding in findings:
                finding = ai_service.enhance_finding(finding, code, language)
        
        # Calculate metrics
        metrics = QualityMetrics(
            total_issues=len(findings),
            critical_issues=sum(1 for f in findings if f.severity.value == 'critical'),
            high_issues=sum(1 for f in findings if f.severity.value == 'high'),
            medium_issues=sum(1 for f in findings if f.severity.value == 'medium'),
            low_issues=sum(1 for f in findings if f.severity.value == 'low'),
            code_quality_score=max(0, 100 - (len(findings) * 5))
        )
        
        # Create result
        result = AnalysisResult(
            file_path='web_input',
            language=language,
            findings=findings,
            metrics=metrics,
            success=True
        )
        
        return jsonify({
            'success': True,
            'result': result.to_dict(),
            'ai_enabled': use_ai and ai_service.is_available()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    """Get AI analysis of code."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        if not ai_service.is_available():
            return jsonify({'error': 'AI service not available. Set GEMINI_API_KEY environment variable.'}), 503
        
        analysis = ai_service.analyze_code_context(code, language)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'ai_available': ai_service.is_available(),
        'supported_languages': parser.get_supported_languages()
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

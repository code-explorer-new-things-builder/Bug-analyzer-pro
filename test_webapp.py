"""Quick test script for web application."""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    data = response.json()
    print(f"✓ Status: {data['status']}")
    print(f"✓ AI Available: {data['ai_available']}")
    print(f"✓ Supported Languages: {', '.join(data['supported_languages'])}")
    print()

def test_analyze():
    """Test code analysis."""
    print("Testing code analysis...")
    
    code = """
def process_data():
    while True:
        print("Processing...")
    return "Done"
"""
    
    payload = {
        "code": code,
        "language": "python",
        "use_ai": False
    }
    
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    data = response.json()
    
    if data['success']:
        result = data['result']
        print(f"✓ Analysis successful")
        print(f"✓ Found {result['metrics']['total_issues']} issues")
        print(f"✓ Quality Score: {result['metrics']['code_quality_score']}")
        
        if result['findings']:
            print(f"\nFindings:")
            for finding in result['findings']:
                print(f"  - Line {finding['line_number']}: {finding['message']} [{finding['severity']}]")
    else:
        print(f"✗ Analysis failed: {data.get('error')}")
    print()

def main():
    """Run all tests."""
    print("=" * 50)
    print("Web Application Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_analyze()
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to server")
        print("Make sure the web app is running: python app.py")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()

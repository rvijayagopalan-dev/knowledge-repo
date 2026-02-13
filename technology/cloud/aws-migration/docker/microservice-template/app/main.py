"""
Sample microservice application
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Configuration
SERVICE_NAME = os.getenv('SERVICE_NAME', 'microservice')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_NAME,
        'environment': ENVIRONMENT
    })


@app.route('/api/info')
def info():
    """Service information endpoint"""
    return jsonify({
        'service': SERVICE_NAME,
        'version': '1.0.0',
        'environment': ENVIRONMENT
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

from flask import Flask
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    logger.info('Received request for /')
    return "Hello World!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting server on port {port}")
    logger.info(f"Environment variables: {dict(os.environ)}")
    app.run(debug=False, host='0.0.0.0', port=port)
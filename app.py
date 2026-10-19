import os
import time
from flask import Flask, jsonify

app = Flask(__name__)
START_TIME = time.time()

@app.route('/')
def index():
    return jsonify({
        "status": "healthy",
        "message": "Welcome to AWS EKS Lab 3 API!",
        "environment": os.getenv("APP_ENV", "development")
    })

@app.route('/healthz')
def healthz():
    return jsonify({"status": "ready", "uptime": time.time() - START_TIME}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
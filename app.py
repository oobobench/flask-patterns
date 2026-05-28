from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# In-memory store
users = {}
sessions = {}

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)

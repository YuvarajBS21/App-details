import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Cloud Run deployment is working!",
        "service": os.environ.get("K_SERVICE", "local"),
        "revision": os.environ.get("K_REVISION", "local"),
    })


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint used by Cloud Run."""
    return jsonify({"status": "healthy"}), 200


@app.route("/echo", methods=["POST"])
def echo():
    """Echo back the JSON body — useful for testing request handling."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    return jsonify({"echo": data}), 200


if __name__ == "__main__":
    # Cloud Run injects the PORT environment variable.
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

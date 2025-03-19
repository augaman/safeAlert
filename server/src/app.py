"""Main application module."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.errorhandler(404)
def not_found_error(error) -> tuple:
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error) -> tuple:
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True) 
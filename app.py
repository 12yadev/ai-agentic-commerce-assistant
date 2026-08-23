from flask import Flask, render_template, request, jsonify
from agent import run_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/api/recommend")
def recommend():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", "")).strip()

    if not query:
        return jsonify({"error": "Please enter a shopping requirement."}), 400

    return jsonify(run_agent(query))

if __name__ == "__main__":
    app.run(debug=True)

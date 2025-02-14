import sys
import os

# Ensure 'backend' is in the path
sys.path.append(os.path.abspath("backend"))

from flask import Flask, render_template, request, jsonify
from backend import computations
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compute', methods=['POST'])
def compute():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Empty request"}), 400

        method = int(data.get("method", 0))
        params = data.get("params", {})

        print(f"✅ Received request: method={method}, params={params}")  # Debug

        # For Task 1 (Plot Graph), call plot_graph() directly
        if method == 1:
            result = computations.plot_graph()  # returns {"graph": ...}
            return jsonify({"graph": result.get("graph")})
        else:
            result = computations.solve(method, params)
            return jsonify({"result": result})
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

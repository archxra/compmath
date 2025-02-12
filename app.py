import sys
import os

# Убедимся, что backend в путях
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

        print(f"✅ Получен запрос: method={method}, params={params}")  # Отладка

        # Если это метод 1 (Plot Graph), вызовем plot_graph() без параметров
        if method == 1:
            result = computations.plot_graph()  # result = {"graph": base64_str}
            # Возвращаем именно строку под ключом graph
            return jsonify({"graph": result.get("graph")})
        else:
            # Для остальных методов вызываем функцию solve(), которая уже вызывает нужный метод
            result = computations.solve(method, params)
            return jsonify({"result": result})
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

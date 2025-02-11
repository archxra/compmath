import sys
import os

# Убедимся, что backend в путях
sys.path.append(os.path.abspath("backend"))

from flask import Flask, render_template, request, jsonify, send_file

try:
    from backend import computations
    print("✅ computations импортирован успешно")
except Exception as e:
    print("❌ Ошибка импорта computations:", e)

import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/compute", methods=["POST"])
def compute():
    try:
        data = request.get_json()
        task_id = data.get("task_id")
        params = data.get("params", {})

        print(f"📌 Получен task_id: {task_id}, параметры: {params}")

        result = computations.solve(task_id, params)  

        print(f"✅ Результат: {result}")

        return jsonify({"success": True, "result": result})

    except Exception as e:
        print(f"❌ Ошибка в обработке запроса: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Используем без GUI
import base64
import io
from io import BytesIO
from scipy.interpolate import CubicSpline
from sympy import symbols, Function, diff, Eq, solve as sym_solve

def solve(task_id, params):
    """Основная функция для выбора метода (для методов, отличных от 1)."""
    methods = {
        2: find_roots,
        3: relaxation_method,
        4: power_method,
        5: exponential_fit,
        6: cubic_spline,
        7: picard_method,
        8: simpsons_rule
    }
    if task_id in methods:
        return format_result(methods[task_id](params))
    return {"error": "Неверный номер задачи"}

def format_result(result):
    """Приводит результаты к user-friendly виду."""
    if isinstance(result, float):
        return round(result, 6)
    elif isinstance(result, list):
        return [round(num, 6) if isinstance(num, (int, float)) else num for num in result]
    elif isinstance(result, dict):
        return {key: format_result(value) for key, value in result.items()}
    return result

def plot_graph():
    x = range(-10, 11)
    y = [i ** 2 for i in x]

    plt.figure()
    plt.plot(x, y, label="y = x^2")
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    
    img_str = base64.b64encode(img.getvalue()).decode()
    print("📸 Полный Base64 перед отправкой:", img_str[:100])
    return {"graph": img_str}

def find_roots(params):
    a = float(params.get('coeffA', 1))
    b = float(params.get('coeffB', 0))
    c = float(params.get('coeffC', 0))

    discriminant = b**2 - 4*a*c
    print(f"📌 Дискриминант: {discriminant}")
    if discriminant < 0:
        return {"roots": "Корней нет (дискриминант < 0)"}
    root1 = (-b + np.sqrt(discriminant)) / (2*a)
    root2 = (-b - np.sqrt(discriminant)) / (2*a)
    result = {"roots": [root1, root2] if root1 != root2 else [root1]}
    print(f"📢 Отправляем ответ: {result}")
    return result

def relaxation_method(params):
    """Метод релаксации для решения уравнения x = f(x)."""
    x0 = float(params.get('x0', 0))
    tol = float(params.get('tol', 1e-6))
    max_iter = int(params.get('max_iter', 100))

    def f(x): return np.cos(x)  # Примерная функция
    
    x = x0
    iterations = 0
    while iterations < max_iter:
        x_next = f(x)
        if abs(x_next - x) < tol:
            return {"solution": x_next, "iterations": iterations}
        x = x_next
        iterations += 1

    return {"solution": "Метод не сошелся", "iterations": max_iter}

def power_method(params):
    """Метод степенного итерационного поиска собственного значения."""
    A = np.array([[float(params['a11']), float(params['a12'])],
                  [float(params['a21']), float(params['a22'])]])
    
    x = np.array([1, 1], dtype=float)
    tol = float(params.get('tol', 1e-6))
    max_iter = int(params.get('max_iter', 100))

    for _ in range(max_iter):
        x_new = np.dot(A, x)
        lambda_approx = max(abs(x_new))
        x_new /= lambda_approx
        
        if np.linalg.norm(x_new - x) < tol:
            return {"eigenvalue": lambda_approx, "eigenvector": x_new.tolist()}
        
        x = x_new

    return {"error": "Метод не сошелся"}

def exponential_fit(params):
    """Экспоненциальная аппроксимация y = a * exp(b * x)."""
    x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])
    y_values = np.array([float(y) for y in params.get('y_values', '').split(',')])

    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Недостаточно данных для аппроксимации"}

    coefficients = np.polyfit(x_values, np.log(y_values), 1)
    a = np.exp(coefficients[1])
    b = coefficients[0]

    return {"a": a, "b": b, "equation": f"y = {a:.4f} * e^({b:.4f}x)"}

def cubic_spline(params):
    """Кубический сплайн-интерполяция."""
    x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])
    y_values = np.array([float(y) for y in params.get('y_values', '').split(',')])

    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Недостаточно точек для интерполяции"}

    cs = CubicSpline(x_values, y_values)
    
    return {"spline_coeffs": cs.c.tolist(), "spline_function": "Готово"}

def picard_method(params):
    """Метод Пикара для решения дифференциальных уравнений."""
    x_val = float(params.get('x', 0.2))
    x = symbols('x')
    y = Function('y')(x)
    f = x + y
    approximations = [1]

    for _ in range(4):
        y_new = 1 + diff(f, x)
        approximations.append(str(y_new))

    return {"approximations": approximations, f"y({x_val})": approximations[-1]}

def simpsons_rule(params):
    """Метод Симпсона для вычисления определенного интеграла."""
    f_values = np.array([float(v) for v in params.get('f_values', '').split(',')])
    x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])

    if len(f_values) < 3 or len(f_values) % 2 == 0:
        return {"error": "Количество точек должно быть нечетным"}

    h = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    integral = (h / 3) * (f_values[0] + 4 * sum(f_values[1:-1:2]) + 2 * sum(f_values[2:-2:2]) + f_values[-1])

    return {"integral": integral, "formatted": f"∫ f(x) dx ≈ {integral:.6f}"}

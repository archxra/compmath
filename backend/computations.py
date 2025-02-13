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
        # Не форматируем график – он уже строка
        formatted = {}
        for key, value in result.items():
            if key == "graph":
                formatted[key] = value
            else:
                formatted[key] = format_result(value)
        return formatted
    return result

def plot_graph():
    """Строит график функции y = x^2."""
    x = range(-10, 11)
    y = [i ** 2 for i in x]

    plt.figure()
    plt.plot(x, y, label="y = x^2", color="blue")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("График функции y = x²")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    
    img_str = base64.b64encode(img.getvalue()).decode()
    print("📸 Полный Base64 перед отправкой (Plot Graph):", img_str[:100])
    return {"graph": img_str}

def find_roots(params):
    """Находит корни уравнения ax² + bx + c = 0 и строит график функции с отмеченными корнями."""
    a = float(params.get('coeffA', 1))
    b = float(params.get('coeffB', 0))
    c = float(params.get('coeffC', 0))

    discriminant = b**2 - 4*a*c
    print(f"📌 Дискриминант: {discriminant}")
    if discriminant < 0:
        return {"roots": "Корней нет (дискриминант < 0)", "graph": ""}
    
    root1 = (-b + np.sqrt(discriminant)) / (2*a)
    root2 = (-b - np.sqrt(discriminant)) / (2*a)
    roots = [root1, root2] if root1 != root2 else [root1]
    
    # Построение графика для функции ax²+bx+c с отмеченными корнями
    x_min = min(roots) - 5
    x_max = max(roots) + 5
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = a * x_vals**2 + b * x_vals + c
    plt.figure()
    plt.plot(x_vals, y_vals, label=f"{a}x² + {b}x + {c}", color="green")
    plt.axhline(0, color='black', linewidth=0.5)
    for r in roots:
        plt.plot(r, 0, "ro", markersize=8)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Нахождение корней квадратичного уравнения")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    result = {"roots": roots, "graph": graph_str}
    print(f"📢 Отправляем ответ (Find Roots): {result}")
    return result

def relaxation_method(params):
    """Метод релаксации для решения уравнения x = f(x) с графиком сходимости.
       Если задан параметр omega, используется формула: x_next = ω·f(x) + (1-ω)·x"""
    x0 = float(params.get('x0', 0))
    tol = float(params.get('tol', 1e-6))
    max_iter = int(params.get('max_iter', 100))
    omega = float(params.get('omega', 1))  # по умолчанию ω = 1 (то есть метод простых итераций)
    
    # Примерная функция: f(x) = cos(x)
    def f(x): 
        return np.cos(x)
    
    iterations_list = [x0]
    x = x0
    count = 0
    while count < max_iter:
        # Если задано ω, используем формулу релаксации:
        x_next = omega * f(x) + (1 - omega) * x
        iterations_list.append(x_next)
        if abs(x_next - x) < tol:
            break
        x = x_next
        count += 1

    # Построение графика сходимости
    plt.figure()
    plt.plot(iterations_list, "o-", color="purple")
    plt.xlabel("Iteration")
    plt.ylabel("x")
    plt.title("Convergence of Relaxation Method")
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    return {"solution": iterations_list[-1], "iterations": count, "iteration_values": iterations_list, "graph": graph_str}

def power_method(params):
    """Метод степенного итерационного поиска собственного значения с графиком сходимости."""
    A = np.array([[float(params['a11']), float(params['a12'])],
                  [float(params['a21']), float(params['a22'])]])
    x = np.array([1, 1], dtype=float)
    tol = float(params.get('tol', 1e-6))
    max_iter = int(params.get('max_iter', 100))
    convergence = [x.copy()]
    for i in range(max_iter):
        x_new = np.dot(A, x)
        lambda_approx = max(abs(x_new))
        x_new /= lambda_approx
        convergence.append(x_new.copy())
        if np.linalg.norm(x_new - x) < tol:
            differences = [np.linalg.norm(convergence[j+1]-convergence[j]) for j in range(len(convergence)-1)]
            plt.figure()
            plt.plot(range(len(differences)), differences, "o-", color="orange")
            plt.xlabel("Номер итерации")
            plt.ylabel("Норма разницы")
            plt.title("Сходимость метода степенных итераций")
            plt.grid()
            img = io.BytesIO()
            plt.savefig(img, format='png', bbox_inches="tight")
            img.seek(0)
            graph_str = base64.b64encode(img.getvalue()).decode()
            return {"eigenvalue": lambda_approx, "eigenvector": x_new.tolist(), "iterations": i, "graph": graph_str}
        x = x_new
    return {"error": "Метод не сошелся"}

def exponential_fit(params):
    """Экспоненциальная аппроксимация y = a * exp(b * x) с графиком подгонки."""
    try:
        x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])
        y_values = np.array([float(y) for y in params.get('y_values', '').split(',')])
    except Exception as e:
        return {"error": "Неверный формат входных данных. Используйте запятые для разделения чисел."}

    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Недостаточно данных для аппроксимации"}
    
    coefficients = np.polyfit(x_values, np.log(y_values), 1)
    a = np.exp(coefficients[1])
    b = coefficients[0]
    
    x_fit = np.linspace(min(x_values), max(x_values), 200)
    y_fit = a * np.exp(b * x_fit)
    plt.figure()
    plt.plot(x_values, y_values, "bo", label="Исходные точки")
    plt.plot(x_fit, y_fit, "r-", label=f"Аппроксимация: y={a:.4f}*exp({b:.4f}x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Экспоненциальная аппроксимация")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    return {"a": a, "b": b, "equation": f"y = {a:.4f} * e^({b:.4f}x)", "graph": graph_str}

def cubic_spline(params):
    """Кубический сплайн-интерполяция с графиком интерполяции."""
    try:
        x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])
        y_values = np.array([float(y) for y in params.get('y_values', '').split(',')])
    except Exception as e:
        return {"error": "Неверный формат входных данных. Используйте запятые для разделения чисел."}
    
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Недостаточно точек для интерполяции"}
    
    cs = CubicSpline(x_values, y_values)
    x_dense = np.linspace(min(x_values), max(x_values), 200)
    y_dense = cs(x_dense)
    plt.figure()
    plt.plot(x_values, y_values, "bo", label="Исходные точки")
    plt.plot(x_dense, y_dense, "r-", label="Сплайн")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Кубическая сплайн-интерполяция")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    return {"spline_coeffs": cs.c.tolist(), "spline_function": "Готово", "graph": graph_str}

def picard_method(params):
    """Метод Пикара для решения дифференциальных уравнений.
       Возвращает таблицу итераций (в виде списка приближений)."""
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
    """Метод Симпсона для вычисления определенного интеграла с графиком разбиения."""
    try:
        x_values = np.array([float(x) for x in params.get('x_values', '').split(',')])
        f_values = np.array([float(v) for v in params.get('f_values', '').split(',')])
    except Exception as e:
        return {"error": "Неверный формат входных данных. Используйте запятые для разделения чисел."}
    
    if len(f_values) < 3 or len(f_values) % 2 == 0:
        return {"error": "Количество точек должно быть нечетным"}
    
    h = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    integral = (h / 3) * (f_values[0] + 4 * sum(f_values[1:-1:2]) + 2 * sum(f_values[2:-2:2]) + f_values[-1])
    
    plt.figure()
    plt.plot(x_values, f_values, "bo-", label="f(x)")
    plt.fill_between(x_values, f_values, color="lightblue", alpha=0.5)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Метод Симпсона")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    
    return {"integral": integral, "formatted": f"∫ f(x) dx ≈ {integral:.6f}", "graph": graph_str}

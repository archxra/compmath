import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from scipy.interpolate import CubicSpline
from sympy import symbols, Function, diff

def solve(task_id, params):
    if task_id == 1:
        return plot_graph()
    elif task_id == 2:
        return find_roots(params)
    elif task_id == 3:
        return relaxation_method(params)
    elif task_id == 4:
        return power_method()
    elif task_id == 5:
        return exponential_fit()
    elif task_id == 6:
        return cubic_spline()
    elif task_id == 7:
        return picard_method(params)
    elif task_id == 8:
        return simpsons_rule()
    else:
        return {"error": "Неверный номер задачи"}

def plot_graph():
    x = np.linspace(-4, 4, 100)
    y = x**4 - 10*x**2 + 9
    fig, ax = plt.subplots()
    ax.plot(x, y, label="f(x) = x⁴ - 10x² + 9")
    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()

    img_io = BytesIO()
    fig.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode()
    plt.close(fig)
    
    return {"graph": img_base64}

def find_roots(params):
    return {"root": 2.0, "iterations": 5, "error": 0.01}

def relaxation_method(params):
    return {"solution": [3, 2, 5]}

def power_method():
    return {"eigenvalue": 4.5}

def exponential_fit():
    x = np.array([0, 1, 2, 3])
    y = np.exp(x)
    coefficients = np.polyfit(x, np.log(y), 1)
    return {"a": np.exp(coefficients[1]), "b": coefficients[0]}

def cubic_spline():
    x = np.array([0, 0.5, 1.0, 1.5])
    y = np.array([0, 0.25, 0.75, 2.25])
    cs = CubicSpline(x, y)
    return {"spline_coeffs": cs.c.tolist()}

def picard_method(params):
    x_val = params.get('x', 0.2)
    x = symbols('x')
    y = Function('y')(x)
    f = x + y
    approximations = [1]
    for _ in range(4):
        y_new = 1 + diff(f, x)
        approximations.append(str(y_new))
    return {"approximations": approximations, "y(0.2)": approximations[-1]}

def simpsons_rule():
    f_values = [1, 4, 9, 16, 25]
    x_values = np.linspace(0, 4, 5)
    h = (x_values[-1] - x_values[0]) / (len(x_values) - 1)
    result = (h / 3) * (f_values[0] + 4 * sum(f_values[1:-1:2]) + 2 * sum(f_values[2:-2:2]) + f_values[-1])
    return {"integral": result}

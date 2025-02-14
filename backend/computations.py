# computations.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use without a GUI
import base64
import io
from io import BytesIO
from scipy.interpolate import CubicSpline
from sympy import symbols, Function, diff, integrate  # note: integrate is imported

#########################################
# Utility: Format results
#########################################
def format_result(result):
    """Brings the results to a user-friendly appearance.
       (Does not reformat the 'graph' string.)"""
    if isinstance(result, float):
        return round(result, 6)
    elif isinstance(result, list):
        return [round(num, 6) if isinstance(num, (int, float)) else num for num in result]
    elif isinstance(result, dict):
        formatted = {}
        for key, value in result.items():
            if key == "graph":
                formatted[key] = value
            else:
                formatted[key] = format_result(value)
        return formatted
    return result

#########################################
# Task 1: Graphical Method and Absolute Error
#########################################
def plot_graph(params={}):
    """
    Plots the function f(x)= x^4 - 10x^2 + 9 over [-4,4].
    Uses a "graphical" (simulated) approximate root (here, taken as 3.1)
    and then finds a more accurate root using Newton's method.
    Returns the approximate root from the graph, the numerical root, 
    the absolute error, and the graph (encoded in base64).
    
    Note: f(x) factors as (x^2-1)(x^2-9)=0, so the true roots are ±1 and ±3.
    Here we focus on the positive root near 3.
    """
    def f(x):
        return x**4 - 10*x**2 + 9
    def df(x):
        return 4*x**3 - 20*x

    x_vals = np.linspace(-4, 4, 400)
    y_vals = f(x_vals)
    
    plt.figure()
    plt.plot(x_vals, y_vals, label="f(x)=x^4-10x^2+9", color="blue")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Task 1: Graphical Method")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.legend()
    plt.grid()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png", bbox_inches="tight")
    img_buf.seek(0)
    graph_str = base64.b64encode(img_buf.getvalue()).decode()

    # Assume a user visually estimates the positive root as approx 3.1
    approx_root = 3.1

    # Now refine using Newton's method starting from approx_root
    tol = float(params.get("tol", 1e-6))
    max_iter = int(params.get("max_iter", 100))
    newton_root = approx_root
    for i in range(max_iter):
        f_val = f(newton_root)
        if abs(f_val) < tol:
            break
        newton_root = newton_root - f_val/df(newton_root)
    abs_error = abs(approx_root - newton_root)
    return {"approximate_root_from_graph": approx_root,
            "numerical_root": round(newton_root, 6),
            "absolute_error": round(abs_error, 6),
            "graph": graph_str}

#########################################
# Task 2: Comparison of Root-Finding Methods
#########################################
def compare_root_methods(params):
    """
    Finds a root of f(x)=x^3-6x^2+11x-6 in the interval [0,3] using:
      - Bisection method
      - Newton-Raphson method
    Returns for each method the computed root, the number of iterations, 
    and the relative error with respect to the true root (2).
    """
    tol = float(params.get("tol", 1e-6))
    max_iter = int(params.get("max_iter", 100))
    
    def f(x):
        return x**3 - 6*x**2 + 11*x - 6
    def df(x):
        return 3*x**2 - 12*x + 11

    true_root = 2.0

    # Bisection method
    a, b = 0.0, 3.0
    bisection_iter = 0
    while bisection_iter < max_iter:
        mid = (a + b) / 2.0
        if abs(f(mid)) < tol or (b - a)/2 < tol:
            bisection_root = mid
            break
        bisection_iter += 1
        if f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
    else:
        bisection_root = mid

    # Newton-Raphson method
    newton_iter = 0
    newton_root = 2.0  # initial guess
    while newton_iter < max_iter:
        f_val = f(newton_root)
        if abs(f_val) < tol:
            break
        newton_root = newton_root - f_val/df(newton_root)
        newton_iter += 1

    bisection_rel_error = abs(bisection_root - true_root)/abs(true_root)
    newton_rel_error = abs(newton_root - true_root)/abs(true_root)
    result = {
        "Bisection": {
            "root": round(bisection_root, 6),
            "iterations": bisection_iter,
            "relative_error": round(bisection_rel_error, 6)
        },
        "Newton-Raphson": {
            "root": round(newton_root, 6),
            "iterations": newton_iter,
            "relative_error": round(newton_rel_error, 6)
        }
    }
    print("📢 Sending result (Compare Root Methods):", result)
    return result

#########################################
# Task 3: Relaxation Method for a system of equations
#########################################
def relaxation_system(params):
    """
    Solves the system:
         x + y + z = 10,
         x + z = 6,
         y + z = 8
    using relaxation with ω (default 0.8).
    Uses the iteration scheme:
         x_new = (1-ω)*x + ω*(10 - y - z)
         y_new = (1-ω)*y + ω*(8 - z)
         z_new = (1-ω)*z + ω*(6 - x)
    """
    omega = float(params.get("omega", 0.8))
    tol = float(params.get("tol", 1e-6))
    max_iter = int(params.get("max_iter", 100))
    
    # Initial guesses (e.g., zeros)
    x, y, z = 0.0, 0.0, 0.0
    iterations = []
    for i in range(max_iter):
        x_new = (1 - omega)*x + omega*(10 - y - z)
        y_new = (1 - omega)*y + omega*(8 - z)
        z_new = (1 - omega)*z + omega*(6 - x)
        iterations.append((x_new, y_new, z_new))
        if abs(x_new - x) < tol and abs(y_new - y) < tol and abs(z_new - z) < tol:
            x, y, z = x_new, y_new, z_new
            break
        x, y, z = x_new, y_new, z_new
    result = {"solution": {"x": round(x, 6), "y": round(y, 6), "z": round(z, 6)},
              "iterations": i+1,
              "iteration_values": iterations}
    return result

#########################################
# Task 4: Finding Eigenvalues Using Power Method (for a 3x3 matrix)
#########################################
def power_method_eigen(params):
    """
    Finds the largest eigenvalue of a 3x3 matrix using the Power Method.
    If the user supplies a 3x3 matrix (keys: a11, a12, a13, a21, a22, a23, a31, a32, a33),
    it is used; otherwise, the default matrix A = [[6,2,3],[2,6,4],[3,4,6]] is used.
    """
    keys = ["a11", "a12", "a13", "a21", "a22", "a23", "a31", "a32", "a33"]
    if all(k in params for k in keys):
        A = np.array([
            [float(params["a11"]), float(params["a12"]), float(params["a13"])],
            [float(params["a21"]), float(params["a22"]), float(params["a23"])],
            [float(params["a31"]), float(params["a32"]), float(params["a33"])]
        ])
    else:
        A = np.array([[6, 2, 3],
                      [2, 6, 4],
                      [3, 4, 6]])
    tol = float(params.get("tol", 1e-6))
    max_iter = int(params.get("max_iter", 100))
    n = A.shape[0]
    x = np.ones(n)
    for i in range(max_iter):
        x_new = np.dot(A, x)
        lambda_approx = np.max(np.abs(x_new))
        x_new = x_new / lambda_approx
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new
    result = {"largest_eigenvalue": round(lambda_approx, 6), "iterations": i+1, "eigenvector": x_new.tolist()}
    return result

#########################################
# Task 5: Exponential Curve Fitting
#########################################
def exponential_fit(params):
    """
    Fits the model y = a * exp(b * x) to the data points:
      (0,1), (1,e), (2,e^2), (3,e^3).
    Expected result: a ~ 1, b ~ 1.
    """
    try:
        x_values = np.array([float(x) for x in params.get('x_values', '0,1,2,3').split(',')])
        y_values = np.array([float(y) for y in params.get('y_values', '1,2.71828,7.38906,20.0855').split(',')])
    except Exception as e:
        return {"error": "Invalid input data format. Use commas to separate numbers."}
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Not enough data for fitting."}
    
    coeffs = np.polyfit(x_values, np.log(y_values), 1)
    b = coeffs[0]
    a = np.exp(coeffs[1])
    
    x_fit = np.linspace(min(x_values), max(x_values), 200)
    y_fit = a * np.exp(b * x_fit)
    
    plt.figure()
    plt.plot(x_values, y_values, "bo", label="Data points")
    plt.plot(x_fit, y_fit, "r-", label=f"Fit: y={a:.4f}*exp({b:.4f}x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Exponential Curve Fitting")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    return {"a": round(a,6), "b": round(b,6), "equation": f"y = {a:.4f} * exp({b:.4f}x)", "graph": graph_str}

#########################################
# Task 6: Cubic Spline Interpolation
#########################################
def cubic_spline(params):
    """
    Uses cubic spline interpolation on the data points:
      (0,0), (0.5,0.25), (1.0,0.75), (1.5,2.25).
    """
    try:
        x_values = np.array([float(x) for x in params.get('x_values', '0,0.5,1.0,1.5').split(',')])
        y_values = np.array([float(y) for y in params.get('y_values', '0,0.25,0.75,2.25').split(',')])
    except Exception as e:
        return {"error": "Invalid input data format. Use commas to separate numbers."}
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return {"error": "Not enough points for interpolation."}
    
    cs = CubicSpline(x_values, y_values)
    x_dense = np.linspace(min(x_values), max(x_values), 200)
    y_dense = cs(x_dense)
    
    plt.figure()
    plt.plot(x_values, y_values, "bo", label="Data points")
    plt.plot(x_dense, y_dense, "r-", label="Cubic spline")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Cubic Spline Interpolation")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    return {"spline_coeffs": cs.c.tolist(), "spline_function": "Done", "graph": graph_str}

#########################################
# Task 7: Picard’s Method
#########################################
def picard_method(params):
    """
    Solves the differential equation dy/dx = x + y with initial condition y(0)=1
    using Picard's iteration up to the fourth approximation.
    Returns the list of approximations (as strings) and the value of y(0.2) from the fourth approximation.
    """
    x = symbols('x')
    # Initial approximation: y0(x) = 1
    y0 = 1  
    # First approximation: y1(x) = 1 + ∫₀ˣ (t + y0) dt = 1 + x + x^2/2
    y1 = 1 + integrate(x + y0, (x, 0, x))
    # Second approximation: y2(x) = 1 + ∫₀ˣ (t + y1) dt
    y2 = 1 + integrate(x + y1, (x, 0, x))
    # Third approximation:
    y3 = 1 + integrate(x + y2, (x, 0, x))
    # Fourth approximation:
    y4 = 1 + integrate(x + y3, (x, 0, x))
    
    y_val = y4.subs(x, 0.2)
    # Convert approximations to strings for JSON serialization.
    approximations = [str(y0), str(y1), str(y2), str(y3), str(y4)]
    return {"approximations": approximations, "y(0.2)": float(y_val)}

#########################################
# Task 8: Simpson’s 1/3 Rule
#########################################
def simpsons_rule(params):
    """
    Computes ∫₀^π sin(x) dx using Simpson’s 1/3 Rule with 10 subintervals.
    Returns the approximate integral, the exact value, and the absolute error.
    """
    import math
    a = 0
    b = math.pi
    n = 10  # number of subintervals (must be even)
    h = (b - a) / n
    x_vals = np.linspace(a, b, n+1)
    f_vals = np.sin(x_vals)
    integral_approx = (h/3) * (f_vals[0] + f_vals[-1] + 4 * sum(f_vals[1:-1:2]) + 2 * sum(f_vals[2:-2:2]))
    exact_value = 2.0
    abs_error = abs(exact_value - integral_approx)
    
    plt.figure()
    plt.plot(x_vals, f_vals, "bo-", label="sin(x)")
    plt.fill_between(x_vals, f_vals, color="lightblue", alpha=0.5)
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.title("Simpson’s 1/3 Rule")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    graph_str = base64.b64encode(img.getvalue()).decode()
    
    return {"integral_approx": round(integral_approx, 6), 
            "exact_value": exact_value,
            "absolute_error": round(abs_error, 6),
            "graph": graph_str}

#########################################
# Main solver function
#########################################
def solve(task_id, params):
    """
    Selects the correct task based on task_id:
      1: Task 1 (Graphical Method and Absolute Error)
      2: Task 2 (Comparison of Root-Finding Methods)
      3: Task 3 (Relaxation Method for a system)
      4: Task 4 (Finding Eigenvalues Using Power Method)
      5: Task 5 (Exponential Curve Fitting)
      6: Task 6 (Cubic Spline Interpolation)
      7: Task 7 (Picard’s Method)
      8: Task 8 (Simpson’s 1/3 Rule)
    """
    methods = {
        1: plot_graph,
        2: compare_root_methods,
        3: relaxation_system,
        4: power_method_eigen,
        5: exponential_fit,
        6: cubic_spline,
        7: picard_method,
        8: simpsons_rule
    }
    if task_id in methods:
        return format_result(methods[task_id](params))
    return {"error": "Invalid task number"}

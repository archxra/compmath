function addExpRow() {
    let tbody = document.getElementById("exp-tbody");
    let newRow = `<tr>
                    <td style="padding:5px;"><input type="number" step="any" style="width:80px;" class="exp-x"></td>
                    <td style="padding:5px;"><input type="number" step="any" style="width:80px;" class="exp-y"></td>
                  </tr>`;
    tbody.insertAdjacentHTML('beforeend', newRow);
}

function addSplineRow() {
    let tbody = document.getElementById("spline-tbody");
    let newRow = `<tr>
                    <td style="padding:5px;"><input type="number" step="any" style="width:80px;" class="spline-x"></td>
                    <td style="padding:5px;"><input type="number" step="any" style="width:80px;" class="spline-y"></td>
                  </tr>`;
    tbody.insertAdjacentHTML('beforeend', newRow);
}

function updateForm() {
    let method = document.getElementById("method").value;
    let formContainer = document.getElementById("dynamic-form");
    formContainer.innerHTML = ""; // Clear the form
  
    // Instructions: "If you leave fields empty, default parameters will be used."
    if (method === "1") { // Task 1: Graphical Method
        formContainer.innerHTML = `
            <p>Graphical Method for f(x)=x^4-10x^2+9 over [-4,4].</p>
            <p>If no values are entered for tolerance and max iterations, defaults are used.</p>
            <label for="tol">Tolerance (ε):</label>
            <input type="number" step="0.000001" id="tol" placeholder="Default: 1e-6">
            <label for="max_iter">Max Iterations:</label>
            <input type="number" id="max_iter" placeholder="Default: 100">
        `;
    } else if (method === "2") { // Task 2: Compare Root Methods
        formContainer.innerHTML = `
            <p>Comparing Bisection and Newton-Raphson for f(x)=x³-6x²+11x-6 in [0,3].</p>
            <p>If fields are empty, default tolerance=1e-6 and max_iter=100 will be used.</p>
            <label for="tol">Tolerance (ε):</label>
            <input type="number" step="0.000001" id="tol" placeholder="Default: 1e-6">
            <label for="max_iter">Max Iterations:</label>
            <input type="number" id="max_iter" placeholder="Default: 100">
        `;
    } else if (method === "3") { // Task 3: Relaxation Method (system)
        formContainer.innerHTML = `
            <p>Solving the system: x+y+z=10, x+z=6, y+z=8 using relaxation.</p>
            <p>If fields are empty, default initial guess = 0, tolerance=1e-6, max_iter=100, ω=0.8 will be used.</p>
            <label for="x0">Initial Guess (x0):</label>
            <input type="number" id="x0" placeholder="Default: 0">
            <label for="tol">Tolerance (ε):</label>
            <input type="number" step="0.000001" id="tol" placeholder="Default: 1e-6">
            <label for="max_iter">Max Iterations:</label>
            <input type="number" id="max_iter" placeholder="Default: 100">
            <label for="omega">Relaxation Coefficient (ω):</label>
            <input type="number" step="0.01" id="omega" placeholder="Default: 0.8">
        `;
    } else if (method === "4") { // Task 4: Power Method for 3x3 Eigenvalue
        formContainer.innerHTML = `
            <p>Enter a 3x3 matrix (optional). If left blank, the default matrix A = [[6,2,3],[2,6,4],[3,4,6]] is used.</p>
            <table style="margin: 0 auto; border-collapse: collapse;">
                <tr>
                    <td style="padding:5px;"><input type="number" id="a11" placeholder="a11" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a12" placeholder="a12" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a13" placeholder="a13" style="width:60px; text-align:center;"></td>
                </tr>
                <tr>
                    <td style="padding:5px;"><input type="number" id="a21" placeholder="a21" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a22" placeholder="a22" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a23" placeholder="a23" style="width:60px; text-align:center;"></td>
                </tr>
                <tr>
                    <td style="padding:5px;"><input type="number" id="a31" placeholder="a31" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a32" placeholder="a32" style="width:60px; text-align:center;"></td>
                    <td style="padding:5px;"><input type="number" id="a33" placeholder="a33" style="width:60px; text-align:center;"></td>
                </tr>
            </table>
            <p>If you leave the matrix fields blank, the default matrix will be used.</p>
            <label for="tol">Tolerance (ε):</label>
            <input type="number" step="0.000001" id="tol" placeholder="Default: 1e-6">
            <label for="max_iter">Max Iterations:</label>
            <input type="number" id="max_iter" placeholder="Default: 100">
        `;
    } else if (method === "5") { // Task 5: Exponential Curve Fitting
        formContainer.innerHTML = `
            <p>Enter data points for exponential curve fitting. If left empty, defaults are used: x: 0,1,2,3; y: 1,e,e^2,e^3.</p>
            <label for="x_values">x values (comma-separated):</label>
            <input type="text" id="x_values" placeholder="e.g. 0,1,2,3">
            <label for="y_values">y values (comma-separated):</label>
            <input type="text" id="y_values" placeholder="e.g. 1,2.71828,7.38906,20.0855">
        `;
    } else if (method === "6") { // Task 6: Cubic Spline Interpolation
        formContainer.innerHTML = `
            <p>Enter data points for cubic spline interpolation. If left empty, defaults are used: x: 0,0.5,1.0,1.5; y: 0,0.25,0.75,2.25.</p>
            <label for="x_values">x values (comma-separated):</label>
            <input type="text" id="x_values" placeholder="e.g. 0,0.5,1.0,1.5">
            <label for="y_values">y values (comma-separated):</label>
            <input type="text" id="y_values" placeholder="e.g. 0,0.25,0.75,2.25">
        `;
    } else if (method === "7") { // Task 7: Picard’s Method
        formContainer.innerHTML = `
            <p>Solve dy/dx = x + y, y(0)=1 up to 4th approximation. (Default values will be used if empty.)</p>
            <label for="picard_x">Evaluate y at x = </label>
            <input type="number" step="0.01" id="picard_x" placeholder="Default: 0.2">
        `;
    } else if (method === "8") { // Task 8: Simpson's Rule
        formContainer.innerHTML = `
            <p>Compute ∫₀^π sin(x) dx using Simpson’s 1/3 Rule with 10 subintervals.</p>
            <p>If no values are entered, default parameters will be used.</p>
            <label for="x_values_integral">x values (comma-separated):</label>
            <input type="text" id="x_values_integral" placeholder="Default: auto-generated over [0,π]">
            <label for="f_values_integral">f(x) values (comma-separated):</label>
            <input type="text" id="f_values_integral" placeholder="Default: sin(x) evaluated">
            <label for="n">Subintervals (odd number of points):</label>
            <input type="number" id="n" min="3" step="2" placeholder="Default: 11">
        `;
    }
}

function compute() {
    let method = document.getElementById("method").value;
    let params = {};

    if (method === "1") { // Task 1
        params = {
            tol: parseFloat(document.getElementById("tol").value) || 1e-6,
            max_iter: parseInt(document.getElementById("max_iter").value) || 100
        };
    } else if (method === "2") { // Task 2
        params = {
            tol: parseFloat(document.getElementById("tol").value) || 1e-6,
            max_iter: parseInt(document.getElementById("max_iter").value) || 100
        };
    } else if (method === "3") { // Task 3
        params = {
            x0: parseFloat(document.getElementById("x0").value) || 0,
            tol: parseFloat(document.getElementById("tol").value) || 1e-6,
            max_iter: parseInt(document.getElementById("max_iter").value) || 100,
            omega: parseFloat(document.getElementById("omega").value) || 0.8
        };
    } else if (method === "4") { // Task 4: Power Method (3x3 matrix)
        // If any field is empty, default values (for default matrix: [[6,2,3],[2,6,4],[3,4,6]]) are used.
        params = {
            a11: document.getElementById("a11").value || "6",
            a12: document.getElementById("a12").value || "2",
            a13: document.getElementById("a13").value || "3",
            a21: document.getElementById("a21").value || "2",
            a22: document.getElementById("a22").value || "6",
            a23: document.getElementById("a23").value || "4",
            a31: document.getElementById("a31").value || "3",
            a32: document.getElementById("a32").value || "4",
            a33: document.getElementById("a33").value || "6",
            tol: parseFloat(document.getElementById("tol").value) || 1e-6,
            max_iter: parseInt(document.getElementById("max_iter").value) || 100
        };
    } else if (method === "5") { // Task 5
        let xs = document.querySelectorAll(".exp-x");
        let ys = document.querySelectorAll(".exp-y");
        let x_values = [];
        let y_values = [];
        xs.forEach(input => { if(input.value !== "") x_values.push(input.value); });
        ys.forEach(input => { if(input.value !== "") y_values.push(input.value); });
        params = {
            x_values: x_values.length ? x_values.join(",") : "0,1,2,3",
            y_values: y_values.length ? y_values.join(",") : "1,2.71828,7.38906,20.0855"
        };
    } else if (method === "6") { // Task 6
        let xs = document.querySelectorAll(".spline-x");
        let ys = document.querySelectorAll(".spline-y");
        let x_values = [];
        let y_values = [];
        xs.forEach(input => { if(input.value !== "") x_values.push(input.value); });
        ys.forEach(input => { if(input.value !== "") y_values.push(input.value); });
        params = {
            x_values: x_values.length ? x_values.join(",") : "0,0.5,1.0,1.5",
            y_values: y_values.length ? y_values.join(",") : "0,0.25,0.75,2.25"
        };
    } else if (method === "7") { // Task 7
        params = {
            x: parseFloat(document.getElementById("picard_x").value) || 0.2
        };
    } else if (method === "8") { // Task 8
        // For Simpson's rule, we use the default: 10 subintervals over [0,π]
        params = {};
    }

    fetch("/compute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ method: parseInt(method), params: params })
    })
    .then(response => response.json())
    .then(data => displayResult(data))
    .catch(error => {
        console.error("❌ Request error:", error);
        document.getElementById("result-table").innerHTML = "<tr><td>❌ Error during request</td></tr>";
    });
}

function displayResult(data) {
    console.log("✅ Server response:", data);
    let resultContainer = document.getElementById("result-table");
    resultContainer.innerHTML = "";

    if (data.error) {
        resultContainer.innerHTML = `<div class="error-message">❌ Error: ${data.error}</div>`;
        return;
    }

    let outputHTML = `<h3>📌 Results:</h3>`;

    // For Task 1: if top-level "graph" exists.
    if (data.graph && typeof data.graph === "string") {
        outputHTML += `<h4>📊 Graph:</h4><img src="data:image/png;base64,${data.graph}" alt="Graph" style="max-width:100%; height:auto;">`;
    }
    // Otherwise, if result is nested (e.g. Task 2)
    else if (data.result) {
        if (data.result.hasOwnProperty("Bisection") || data.result.hasOwnProperty("Newton-Raphson")) {
            for (let method in data.result) {
                let subResult = data.result[method];
                outputHTML += `<h4>🔹 ${method}:</h4>`;
                outputHTML += `<table border="1" style="width:100%; margin-bottom:10px;"><tbody>`;
                for (let key in subResult) {
                    let value = subResult[key];
                    if (typeof value === "number") {
                        outputHTML += `<tr><td><strong>${key}</strong></td><td>${value.toFixed(6)}</td></tr>`;
                    } else if (Array.isArray(value)) {
                        outputHTML += `<tr><td><strong>${key}</strong></td><td>${value.join(", ")}</td></tr>`;
                    } else {
                        outputHTML += `<tr><td><strong>${key}</strong></td><td>${value}</td></tr>`;
                    }
                }
                outputHTML += `</tbody></table>`;
            }
        } else {
            if (data.result.graph && typeof data.result.graph === "string") {
                outputHTML += `<h4>📊 Graph:</h4><img src="data:image/png;base64,${data.result.graph}" alt="Graph" style="max-width:100%; height:auto;">`;
            }
            for (let key in data.result) {
                if (key === "graph") continue;
                let value = data.result[key];
                if (key === "roots" && Array.isArray(value)) {
                    outputHTML += `<h4>🔹 ${key}:</h4><table border="1"><tbody>`;
                    value.forEach(root => {
                        outputHTML += `<tr><td>${root.toFixed(6)}</td></tr>`;
                    });
                    outputHTML += `</tbody></table>`;
                } else if (typeof value === "number") {
                    outputHTML += `<p>✅ <strong>${key}:</strong> ${value.toFixed(6)}</p>`;
                } else if (Array.isArray(value)) {
                    outputHTML += `<h4>🔹 ${key}:</h4><table border="1"><tbody>`;
                    value.forEach(item => {
                        outputHTML += `<tr><td>${item}</td></tr>`;
                    });
                    outputHTML += `</tbody></table>`;
                } else {
                    outputHTML += `<p>🔹 <strong>${key}:</strong> ${value}</p>`;
                }
            }
        }
    }

    resultContainer.innerHTML = outputHTML;
}

function clearForm() {
    document.getElementById("dynamic-form").innerHTML = "";
    document.getElementById("graph-container").innerHTML = "";
    document.getElementById("result-table").innerHTML = "";
}

document.addEventListener("DOMContentLoaded", function() {
    let computeBtn = document.getElementById("compute-button");
    if (computeBtn) {
        computeBtn.addEventListener("click", compute);
    } else {
        console.error("Calculate button not found!");
    }
});

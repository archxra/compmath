function updateForm() {
    let method = document.getElementById("method").value;
    let formContainer = document.getElementById("dynamic-form");
    formContainer.innerHTML = ""; // Очищаем форму

    if (method === "1") { // Plot Graph
        formContainer.innerHTML = "<p>График функции будет построен автоматически.</p>";
    } else if (method === "2") { // Find Roots
        formContainer.innerHTML = `
            <label for="coeffA">Coefficient A:</label>
            <input type="number" id="coeffA">
            <label for="coeffB">Coefficient B:</label>
            <input type="number" id="coeffB">
            <label for="coeffC">Coefficient C:</label>
            <input type="number" id="coeffC">
        `;
    } else if (method === "3") { // Relaxation Method
        formContainer.innerHTML = `
            <label for="x0">Initial Guess (x0):</label>
            <input type="number" id="x0">
            <label for="tol">Tolerance:</label>
            <input type="number" step="0.000001" id="tol">
            <label for="max_iter">Max Iterations:</label>
            <input type="number" id="max_iter">
        `;
    } else if (method === "4") { // Power Method
        formContainer.innerHTML = `
            <div style="margin-bottom: 10px;">
                <p style="font-weight: bold;">Введите значения для матрицы 2x2:</p>
                <table style="margin: 0; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 5px;">
                            <input type="number" id="a11" placeholder="A11" style="width: 60px; text-align: center;">
                        </td>
                        <td style="padding: 5px;">
                            <input type="number" id="a12" placeholder="A12" style="width: 60px; text-align: center;">
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;">
                            <input type="number" id="a21" placeholder="A21" style="width: 60px; text-align: center;">
                        </td>
                        <td style="padding: 5px;">
                            <input type="number" id="a22" placeholder="A22" style="width: 60px; text-align: center;">
                        </td>
                    </tr>
                </table>
            </div>
            <div style="margin-top: 10px;">
                <label for="tol_power">Tolerance:</label>
                <input type="number" step="0.000001" id="tol_power" style="width: 100px; margin-right: 10px;">
                <label for="max_iter_power">Max Iterations:</label>
                <input type="number" id="max_iter_power" style="width: 80px;">
            </div>
        `;    
    } else if (method === "5") { // Exponential Fit
        formContainer.innerHTML = `
            <label for="x_values">x values (comma-separated):</label>
            <input type="text" id="x_values">
            <label for="y_values">y values (comma-separated):</label>
            <input type="text" id="y_values">
        `;
    } else if (method === "6") { // Cubic Spline
        formContainer.innerHTML = `
            <label for="x_values_spline">x values (comma-separated):</label>
            <input type="text" id="x_values_spline">
            <label for="y_values_spline">y values (comma-separated):</label>
            <input type="text" id="y_values_spline">
        `;
    } else if (method === "7") { // Picard Method
        formContainer.innerHTML = `
            <label for="picard_x">x value:</label>
            <input type="number" step="0.01" id="picard_x">
        `;
    } else if (method === "8") { // Simpson's Rule
        formContainer.innerHTML = `
            <label for="integral-func">Function (not used here, placeholder):</label>
            <input type="text" id="integral-func">
            <label for="a">Lower Limit:</label>
            <input type="number" id="a">
            <label for="b">Upper Limit:</label>
            <input type="number" id="b">
            <label for="n">Subintervals (even number):</label>
            <input type="number" id="n" min="2" step="2">
        `;
    }
}

function generateMatrix() {
    let size = document.getElementById("matrix-size").value;
    let container = document.getElementById("matrix-container");
    container.innerHTML = "";
    let table = document.createElement("table");

    for (let i = 0; i < size; i++) {
        let row = document.createElement("tr");
        for (let j = 0; j < size; j++) {
            let cell = document.createElement("td");
            let input = document.createElement("input");
            input.type = "number";
            input.id = `matrix-${i}-${j}`;
            cell.appendChild(input);
            row.appendChild(cell);
        }
        table.appendChild(row);
    }

    container.appendChild(table);
}

function compute() {
    let method = document.getElementById("method").value;
    let params = {};

    if (method === "2") { // Find Roots
        params = {
            coeffA: parseFloat(document.getElementById("coeffA").value),
            coeffB: parseFloat(document.getElementById("coeffB").value),
            coeffC: parseFloat(document.getElementById("coeffC").value)
        };
    } else if (method === "3") { // Relaxation Method
        params = {
            x0: parseFloat(document.getElementById("x0").value),
            tol: parseFloat(document.getElementById("tol").value),
            max_iter: parseInt(document.getElementById("max_iter").value)
        };
    } else if (method === "4") { // Power Method
        params = {
            a11: parseFloat(document.getElementById("a11").value),
            a12: parseFloat(document.getElementById("a12").value),
            a21: parseFloat(document.getElementById("a21").value),
            a22: parseFloat(document.getElementById("a22").value),
            tol: parseFloat(document.getElementById("tol_power").value),
            max_iter: parseInt(document.getElementById("max_iter_power").value)
        };
    } else if (method === "5") { // Exponential Fit
        params = {
            x_values: document.getElementById("x_values").value,
            y_values: document.getElementById("y_values").value
        };
    } else if (method === "6") { // Cubic Spline
        params = {
            x_values: document.getElementById("x_values_spline").value,
            y_values: document.getElementById("y_values_spline").value
        };
    } else if (method === "7") { // Picard Method
        params = {
            x: parseFloat(document.getElementById("picard_x").value)
        };
    } else if (method === "8") { // Simpson's Rule
        params = {
            func: document.getElementById("integral-func").value,
            a: parseFloat(document.getElementById("a").value),
            b: parseFloat(document.getElementById("b").value),
            n: parseInt(document.getElementById("n").value)
        };
    }

    // Далее отправка AJAX-запроса, как у тебя уже реализована...
    fetch("/compute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ method: method, params: params })
    })
    .then(response => response.json())
    .then(data => displayResult(data))
    .catch(error => {
        console.error("❌ Ошибка запроса:", error);
        document.getElementById("result-table").innerHTML = "<tr><td>❌ Ошибка при запросе к серверу</td></tr>";
    });
}

function displayResult(data) {
    console.log("✅ Ответ сервера:", data);
    let resultContainer = document.getElementById("result-table");
    resultContainer.innerHTML = "";

    if (data.error) {
        resultContainer.innerHTML = `<div class="error-message">❌ Ошибка: ${data.error}</div>`;
        return;
    }

    let outputHTML = `<h3>📌 Результаты вычислений:</h3>`;

    // Если метод 1, график возвращается напрямую в data.graph
    if (data.graph && typeof data.graph === "string") {
        outputHTML += `<h4>📊 График:</h4><img src="data:image/png;base64,${data.graph}" alt="Graph" style="max-width:100%; height:auto;">`;
    }
    // Если метод не 1, результат находится в data.result
    else if (data.result) {
        // Если в data.result есть график, выводим его как изображение
        if (data.result.graph && typeof data.result.graph === "string") {
            outputHTML += `<h4>📊 График:</h4><img src="data:image/png;base64,${data.result.graph}" alt="Graph" style="max-width:100%; height:auto;">`;
        }
        // Выводим остальные данные
        for (let key in data.result) {
            // Пропускаем ключ "graph", если он уже обработан
            if (key === "graph") continue;
            let value = data.result[key];
            if (key === "roots" && Array.isArray(value)) {
                outputHTML += `<h4>🔹 ${key}:</h4><table><tbody>`;
                value.forEach(root => {
                    outputHTML += `<tr><td>${root.toFixed(6)}</td></tr>`;
                });
                outputHTML += `</tbody></table>`;
            } else if (typeof value === "number") {
                outputHTML += `<p>✅ <strong>${key}:</strong> ${value.toFixed(6)}</p>`;
            } else if (Array.isArray(value)) {
                outputHTML += `<h4>🔹 ${key}:</h4><table><tbody>`;
                value.forEach(item => {
                    outputHTML += `<tr><td>${item}</td></tr>`;
                });
                outputHTML += `</tbody></table>`;
            } else {
                outputHTML += `<p>🔹 <strong>${key}:</strong> ${value}</p>`;
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
        console.error("Кнопка Calculate не найдена!");
    }
});
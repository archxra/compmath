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
    } else if (method === "3") { // Relaxation
        formContainer.innerHTML = `
            <label for="matrix-size">Matrix Size:</label>
            <input type="number" id="matrix-size" value="3" min="2" max="10" onchange="generateMatrix()">
            <div id="matrix-container"></div>
        `;
        generateMatrix();
    } else if (method === "8") { // Simpson's Rule
        formContainer.innerHTML = `
            <label for="integral-func">Function:</label>
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
    let table = document.getElementById("result-table");
    let graphContainer = document.getElementById("graph-container");

    if (!table || !graphContainer) {
        console.error("❌ Ошибка: Не найдены элементы для вывода!");
        return;
    }

    table.innerHTML = "<tr><td>⌛ Обрабатываем запрос...</td></tr>";

    let params = {};
    if (method === "2") { // Find Roots
        params = {
            coeffA: parseFloat(document.getElementById("coeffA").value),
            coeffB: parseFloat(document.getElementById("coeffB").value),
            coeffC: parseFloat(document.getElementById("coeffC").value),
        };
    } else if (method === "8") { // Simpson's Rule
        params = {
            func: document.getElementById("integral-func").value,
            a: parseFloat(document.getElementById("a").value),
            b: parseFloat(document.getElementById("b").value),
            n: parseInt(document.getElementById("n").value),
        };
    }

    fetch("/compute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ method: method, params: params })
    })
    .then(response => response.json())
    .then(data => displayResult(data))
    .catch(error => {
        console.error("❌ Ошибка запроса:", error);
        table.innerHTML = "<tr><td>❌ Ошибка при запросе к серверу</td></tr>";
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

    // Если приходит график, выводим его
    if (data.graph && typeof data.graph === "string") {
        outputHTML += `<h4>📊 График:</h4><img src="data:image/png;base64,${data.graph}" alt="Graph" style="max-width:100%; height:auto;">`;
    }
    // Если результат находится в data.result, обрабатываем его
    else if (data.result) {
        // Если data.result является объектом, можно его распечатать
        for (let key in data.result) {
            let value = data.result[key];
            if (key === "roots" && Array.isArray(value)) {
                outputHTML += `<h4>🔹 ${key}:</h4><table><tbody>`;
                value.forEach(root => {
                    outputHTML += `<tr><td>${root.toFixed(6)}</td></tr>`;
                });
                outputHTML += `</tbody></table>`;
            } else if (typeof value === "number") {
                outputHTML += `<p>✅ <strong>${key}:</strong> ${value.toFixed(6)}</p>`;
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
const flowCount = document.getElementById("flow-count");
const anomalyRatio = document.getElementById("anomaly-ratio");
const generateButton = document.getElementById("generate-button");
const refreshButton = document.getElementById("refresh-button");
const summary = document.getElementById("summary");
const tableContainer = document.getElementById("table-container");

async function apiRequest(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json();
    throw new Error(payload.detail || "Erreur API");
  }
  return response.json();
}

function renderSummary(data) {
  summary.textContent = `Total: ${data.summary.total} | Anomalies: ${data.summary.anomalies} (${(
    data.summary.anomaly_ratio * 100
  ).toFixed(1)}%)`;
}

function renderTable(items) {
  const table = document.createElement("table");
  table.innerHTML = `
    <thead>
      <tr>
        <th>Timestamp</th>
        <th>Src</th>
        <th>Dest</th>
        <th>Port</th>
        <th>Bytes</th>
        <th>Label</th>
        <th>Prédiction</th>
        <th>Score</th>
      </tr>
    </thead>
  `;
  const tbody = document.createElement("tbody");
  items.slice(0, 120).forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${item.timestamp}</td>
      <td>${item.src_ip}</td>
      <td>${item.dest_ip}</td>
      <td>${item.dest_port}</td>
      <td>${item.bytes_out}</td>
      <td>${item.label}</td>
      <td class="${item.prediction}">${item.prediction}</td>
      <td>${item.score.toFixed(3)}</td>
    `;
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
  tableContainer.innerHTML = "";
  tableContainer.appendChild(table);
}

async function fetchLatest() {
  const data = await apiRequest("/api/detections");
  renderSummary(data);
  renderTable(data.items);
}

generateButton.addEventListener("click", async () => {
  summary.textContent = "Génération en cours...";
  try {
    const data = await apiRequest("/api/generate", {
      method: "POST",
      body: JSON.stringify({
        count: Number(flowCount.value),
        anomaly_ratio: Number(anomalyRatio.value),
      }),
    });
    renderSummary(data);
    renderTable(data.items);
  } catch (err) {
    summary.textContent = `Erreur: ${err.message}`;
  }
});

refreshButton.addEventListener("click", () => {
  fetchLatest().catch((err) => {
    summary.textContent = `Erreur: ${err.message}`;
  });
});

const createButton = document.getElementById("create-button");
const refreshButton = document.getElementById("refresh-button");
const itemName = document.getElementById("item-name");
const itemOwner = document.getElementById("item-owner");
const itemsList = document.getElementById("items-list");

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

async function loadItems() {
  itemsList.textContent = "Chargement...";
  const data = await apiRequest("/api/items");
  itemsList.innerHTML = "";
  if (data.items.length === 0) {
    itemsList.textContent = "Aucun item.";
    return;
  }
  data.items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "item";
    card.innerHTML = `
      <div>
        <strong>${item.name}</strong>
        <span>(${item.owner})</span>
      </div>
      <button data-id="${item.id}">Supprimer</button>
    `;
    card.querySelector("button").addEventListener("click", async () => {
      await apiRequest(`/api/items/${item.id}`, { method: "DELETE" });
      await loadItems();
    });
    itemsList.appendChild(card);
  });
}

createButton.addEventListener("click", async () => {
  const name = itemName.value.trim();
  const owner = itemOwner.value.trim();
  if (!name || !owner) {
    alert("Nom et owner requis.");
    return;
  }
  await apiRequest("/api/items", {
    method: "POST",
    body: JSON.stringify({ name, owner }),
  });
  itemName.value = "";
  itemOwner.value = "";
  await loadItems();
});

refreshButton.addEventListener("click", loadItems);

loadItems().catch((err) => {
  itemsList.textContent = `Erreur: ${err.message}`;
});

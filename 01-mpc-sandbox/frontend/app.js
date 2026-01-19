const splitSecret = document.getElementById("split-secret");
const splitThreshold = document.getElementById("split-threshold");
const splitShares = document.getElementById("split-shares");
const splitButton = document.getElementById("split-button");
const splitOutput = document.getElementById("split-output");

const combineShares = document.getElementById("combine-shares");
const combineButton = document.getElementById("combine-button");
const combineOutput = document.getElementById("combine-output");

const signMessage = document.getElementById("sign-message");
const signShares = document.getElementById("sign-shares");
const signButton = document.getElementById("sign-button");
const signOutput = document.getElementById("sign-output");

const pretty = (value) => JSON.stringify(value, null, 2);

async function apiRequest(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Erreur API");
  }
  return data;
}

splitButton.addEventListener("click", async () => {
  splitOutput.textContent = "Génération en cours...";
  try {
    const data = await apiRequest("/api/split", {
      secret: splitSecret.value.trim(),
      threshold: Number(splitThreshold.value),
      shares: Number(splitShares.value),
      encoding: "utf-8",
    });

    splitOutput.textContent = pretty(data);
    const sharesJson = pretty(data.shares_data);
    combineShares.value = sharesJson;
    signShares.value = sharesJson;
  } catch (err) {
    splitOutput.textContent = `Erreur: ${err.message}`;
  }
});

combineButton.addEventListener("click", async () => {
  combineOutput.textContent = "Reconstruction en cours...";
  try {
    const sharesPayload = JSON.parse(combineShares.value);
    const data = await apiRequest("/api/combine", {
      shares: sharesPayload,
      encoding: "utf-8",
    });
    combineOutput.textContent = pretty(data);
  } catch (err) {
    combineOutput.textContent = `Erreur: ${err.message}`;
  }
});

signButton.addEventListener("click", async () => {
  signOutput.textContent = "Signature en cours...";
  try {
    const sharesPayload = JSON.parse(signShares.value);
    const data = await apiRequest("/api/sign", {
      message: signMessage.value.trim(),
      shares: sharesPayload,
      encoding: "utf-8",
    });
    signOutput.textContent = pretty(data);
  } catch (err) {
    signOutput.textContent = `Erreur: ${err.message}`;
  }
});

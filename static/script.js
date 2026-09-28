const form = document.getElementById("trip-form");
const btn = document.getElementById("generate-btn");
const btnText = btn.querySelector(".btn-text");
const spinner = btn.querySelector(".spinner");
const resultSection = document.getElementById("result");
const itineraryText = document.getElementById("itinerary-text");
const errorBox = document.getElementById("error");
const downloadBtn = document.getElementById("download-btn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();
  setLoading(true);

  const payload = {
    name: document.getElementById("name").value.trim(),
    destination: document.getElementById("destination").value.trim(),
    days: parseInt(document.getElementById("days").value, 10),
    budget: parseInt(document.getElementById("budget").value, 10),
    interests: document
      .getElementById("interests")
      .value.split(",")
      .map((s) => s.trim())
      .filter(Boolean),
    travel_style: document.getElementById("travel_style").value,
    technique: document.getElementById("technique").value,
  };

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Request failed (${res.status})`);
    }

    const data = await res.json();
    itineraryText.textContent = data.itinerary;
    resultSection.hidden = false;
    resultSection.scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    showError(err.message);
  } finally {
    setLoading(false);
  }
});

downloadBtn.addEventListener("click", () => {
  const blob = new Blob([itineraryText.textContent], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `itinerary-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
});

function setLoading(loading) {
  btn.disabled = loading;
  spinner.hidden = !loading;
  btnText.textContent = loading ? "Generating..." : "Generate Itinerary";
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.hidden = false;
}

function hideError() {
  errorBox.hidden = true;
}
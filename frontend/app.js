const form = document.getElementById("business-form");
const generateButton = document.getElementById("generate");
const welcome = document.getElementById("welcome");
const loading = document.getElementById("loading");
const output = document.getElementById("output");
const errorBox = document.getElementById("error");
const resultText = document.getElementById("result-text");

const titles = {
  audience: "Audience Finder",
  strategy: "Marketing Strategy",
  content: "Content Studio",
  outreach: "Customer Outreach"
};

let activeFeature = "audience";

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    activeFeature = button.dataset.feature;

    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.toggle("active", item === button);
    });

    document.getElementById("crumb").textContent =
      titles[activeFeature];

    document.getElementById("result-title").textContent =
      titles[activeFeature];

    welcome.classList.remove("hidden");
    output.classList.add("hidden");
    errorBox.classList.add("hidden");

    welcome.querySelector("h3").textContent =
      `${titles[activeFeature]} is ready`;

    welcome.querySelector("p").textContent =
      "Complete your business profile and generate a tailored starting point.";
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = Object.fromEntries(new FormData(form).entries());

  if (!data.location.trim()) data.location = "Not specified";
  if (!data.audience.trim()) data.audience = "Not sure yet";

  generateButton.disabled = true;
  welcome.classList.add("hidden");
  output.classList.add("hidden");
  errorBox.classList.add("hidden");
  loading.classList.remove("hidden");

  try {
    const response = await fetch(`/api/${activeFeature}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "Unable to generate results."
      );
    }

    resultText.textContent = result.result;

    document.getElementById("provider-label").textContent =
      result.provider === "huggingface"
        ? "OPEN-WEIGHT MODEL INFERENCE"
        : "DEMO OUTPUT — NOT AI-GENERATED";

    document.getElementById("disclaimer").textContent =
      result.disclaimer;

    output.classList.remove("hidden");
  } catch (error) {
    errorBox.textContent =
      "Could not generate results: " + error.message;
    errorBox.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
    generateButton.disabled = false;
  }
});

document.getElementById("copy").addEventListener("click", async () => {
  const button = document.getElementById("copy");

  try {
    await navigator.clipboard.writeText(resultText.textContent);
    button.textContent = "Copied!";
    setTimeout(() => {
      button.textContent = "Copy results";
    }, 1500);
  } catch {
    button.textContent = "Select and copy text";
  }
});
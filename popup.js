const DEFAULT_SETTINGS = Object.freeze({
  enabled: true
});

const toggle = document.querySelector("#enabledToggle");
const statusText = document.querySelector("#statusText");

void loadSettings();

toggle.addEventListener("change", async (event) => {
  const enabled = event.target.checked;

  applyState(enabled);

  try {
    await chrome.storage.sync.set({
      enabled
    });
  } catch (error) {
    console.error("Failed to persist popup state", error);
  }
});

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== "sync" || !changes.enabled) {
    return;
  }

  applyState(changes.enabled.newValue !== false);
});

async function loadSettings() {
  try {
    const settings = await chrome.storage.sync.get(DEFAULT_SETTINGS);
    applyState(settings.enabled !== false);
  } catch (error) {
    console.error("Failed to load popup state", error);
    applyState(DEFAULT_SETTINGS.enabled);
  }
}

function applyState(enabled) {
  toggle.checked = enabled;
  statusText.textContent = enabled ? "On" : "Off";
  document.body.dataset.enabled = String(enabled);
}

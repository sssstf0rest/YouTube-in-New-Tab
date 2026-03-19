# Implementation Guide

This repository now includes a working no-build Manifest V3 scaffold. The code below matches the live files in the project root.

## Extension Files

### `manifest.json`

```json
{
  "manifest_version": 3,
  "name": "YouTube in New Tab",
  "version": "0.1.0",
  "description": "Open YouTube video watch links in a new tab on plain left-click.",
  "permissions": ["storage"],
  "background": {
    "service_worker": "service-worker.js"
  },
  "icons": {
    "16": "icons/icon-16.png",
    "32": "icons/icon-32.png",
    "48": "icons/icon-48.png",
    "128": "icons/icon-128.png"
  },
  "action": {
    "default_title": "YouTube in New Tab",
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon-16.png",
      "32": "icons/icon-32.png"
    }
  },
  "content_scripts": [
    {
      "matches": ["https://www.youtube.com/*"],
      "js": ["content.js"],
      "run_at": "document_start"
    }
  ]
}
```

### `service-worker.js`

```js
const OPEN_VIDEO_TAB = "OPEN_VIDEO_TAB";
const DEFAULT_SETTINGS = Object.freeze({
  enabled: true
});

chrome.runtime.onInstalled.addListener(async () => {
  const settings = await chrome.storage.sync.get(DEFAULT_SETTINGS);

  if (typeof settings.enabled !== "boolean") {
    await chrome.storage.sync.set(DEFAULT_SETTINGS);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || message.type !== OPEN_VIDEO_TAB) {
    return false;
  }

  void (async () => {
    try {
      const url = validateVideoUrl(message.url);
      const createProperties = {
        url: url.toString(),
        active: true
      };

      if (typeof sender.tab?.windowId === "number") {
        createProperties.windowId = sender.tab.windowId;
      }

      if (typeof sender.tab?.index === "number") {
        createProperties.index = sender.tab.index + 1;
      }

      if (typeof sender.tab?.id === "number") {
        createProperties.openerTabId = sender.tab.id;
      }

      const tab = await chrome.tabs.create(createProperties);

      sendResponse({
        ok: true,
        tabId: tab.id
      });
    } catch (error) {
      console.error("Failed to open YouTube tab", error);
      sendResponse({
        ok: false,
        error: error instanceof Error ? error.message : String(error)
      });
    }
  })();

  return true;
});

function validateVideoUrl(rawUrl) {
  const url = new URL(rawUrl);

  if (url.origin !== "https://www.youtube.com") {
    throw new Error("Only https://www.youtube.com watch links are allowed.");
  }

  if (url.pathname !== "/watch") {
    throw new Error("Only /watch links are supported in v1.");
  }

  if (!url.searchParams.has("v")) {
    throw new Error("Missing required video id parameter.");
  }

  return url;
}
```

### `content.js`

```js
const OPEN_VIDEO_TAB = "OPEN_VIDEO_TAB";
const DEFAULT_SETTINGS = Object.freeze({
  enabled: true
});

let extensionEnabled = DEFAULT_SETTINGS.enabled;

void initializeEnabledState();

document.addEventListener("click", handleDocumentClick, true);

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== "sync" || !changes.enabled) {
    return;
  }

  extensionEnabled = changes.enabled.newValue !== false;
});

async function initializeEnabledState() {
  try {
    const settings = await chrome.storage.sync.get(DEFAULT_SETTINGS);
    extensionEnabled = settings.enabled !== false;
  } catch (error) {
    console.error("Failed to load extension settings", error);
    extensionEnabled = DEFAULT_SETTINGS.enabled;
  }
}

function handleDocumentClick(event) {
  if (!extensionEnabled || isCurrentPageWatchVideo() || !shouldInterceptClick(event)) {
    return;
  }

  const anchor = getAnchorFromEvent(event);

  if (!anchor || isTargetBlank(anchor)) {
    return;
  }

  const url = toSupportedVideoUrl(anchor.href);

  if (!url) {
    return;
  }

  event.preventDefault();
  event.stopImmediatePropagation();

  void chrome.runtime
    .sendMessage({
      type: OPEN_VIDEO_TAB,
      url: url.toString()
    })
    .then((response) => {
      if (response?.ok) {
        return;
      }

      throw new Error(response?.error || "Unknown runtime error");
    })
    .catch((error) => {
      console.error("Failed to open YouTube video in a new tab", error);
      window.location.assign(url.toString());
    });
}

function shouldInterceptClick(event) {
  return (
    event.isTrusted &&
    !event.defaultPrevented &&
    event.button === 0 &&
    !event.metaKey &&
    !event.ctrlKey &&
    !event.shiftKey &&
    !event.altKey
  );
}

function isCurrentPageWatchVideo() {
  return window.location.pathname === "/watch" && new URLSearchParams(window.location.search).has("v");
}

function getAnchorFromEvent(event) {
  if (typeof event.composedPath === "function") {
    for (const node of event.composedPath()) {
      const anchor = getClosestAnchor(node);

      if (anchor) {
        return anchor;
      }
    }
  }

  return getClosestAnchor(event.target);
}

function getClosestAnchor(node) {
  if (!(node instanceof Element)) {
    return null;
  }

  if (node instanceof HTMLAnchorElement && node.href) {
    return node;
  }

  return node.closest("a[href]");
}

function isTargetBlank(anchor) {
  return anchor.target.toLowerCase() === "_blank";
}

function toSupportedVideoUrl(rawHref) {
  let url;

  try {
    url = new URL(rawHref, window.location.origin);
  } catch {
    return null;
  }

  if (url.origin !== window.location.origin) {
    return null;
  }

  if (url.pathname !== "/watch") {
    return null;
  }

  if (!url.searchParams.has("v")) {
    return null;
  }

  return url;
}
```

### `popup.html`

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>YouTube in New Tab</title>
    <link rel="stylesheet" href="popup.css" />
  </head>
  <body>
    <main class="popup">
      <div class="header">
        <span class="icon-mark" aria-hidden="true">Y</span>
        <div class="header-copy">
          <h1 class="title">YouTube in New Tab</h1>
          <p class="summary">Open YouTube video links in a new tab.</p>
        </div>
      </div>

      <label class="toggle-row" for="enabledToggle">
        <span class="toggle-copy">
          <span class="toggle-label">Enabled</span>
          <span class="toggle-note">Works on feed, search, and channel pages. Disabled on open video pages.</span>
        </span>

        <span class="toggle-shell">
          <input id="enabledToggle" class="toggle-input" type="checkbox" />
          <span class="toggle-track" aria-hidden="true">
            <span class="toggle-thumb"></span>
          </span>
        </span>
      </label>

      <div class="status-row" aria-live="polite">
        <span class="status-label">Status</span>
        <span id="statusText" class="status-pill">On</span>
      </div>
    </main>

    <script src="popup.js"></script>
  </body>
</html>
```

### `popup.css`

```css
:root {
  color-scheme: light;
  --red: #d71920;
  --red-dark: #ac0f17;
  --red-soft: #ffe7e8;
  --white: #ffffff;
  --line: #f2c7cb;
  --text: #231315;
  --muted: #6f4a4e;
  --shadow: 0 10px 24px rgba(215, 25, 32, 0.14);
  --body-font: "Avenir Next", "Segoe UI", sans-serif;
  --mono-font: "SF Mono", "JetBrains Mono", "Cascadia Code", Consolas, monospace;
}

* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-width: 296px;
}

body {
  padding: 12px;
  color: var(--text);
  font-family: var(--body-font);
  background: linear-gradient(180deg, #fff5f5 0%, #ffffff 100%);
}

.popup {
  padding: 14px;
  border: 1px solid var(--line);
  border-top: 5px solid var(--red);
  border-radius: 16px;
  background: var(--white);
  box-shadow: var(--shadow);
}

.header {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 14px;
}

.title {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
}

.summary {
  margin: 0;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}

.icon-mark {
  display: inline-grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 2px solid var(--red);
  border-radius: 10px;
  background: var(--white);
  color: var(--red);
  font-size: 22px;
  font-weight: 800;
  line-height: 1;
}

.toggle-row {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--red-soft);
  cursor: pointer;
}

.toggle-copy {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.toggle-label {
  font-size: 13px;
  font-weight: 700;
}

.toggle-note {
  color: var(--muted);
  font-size: 11px;
  line-height: 1.4;
}

.toggle-note code {
  padding: 0.1rem 0.32rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  font-family: var(--mono-font);
  font-size: 11px;
}

.toggle-shell {
  position: relative;
  flex: 0 0 auto;
}

.toggle-input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.toggle-track {
  display: inline-flex;
  align-items: center;
  width: 52px;
  height: 30px;
  padding: 3px;
  border-radius: 999px;
  background: rgba(215, 25, 32, 0.2);
  box-shadow: inset 0 0 0 1px rgba(215, 25, 32, 0.16);
  transition: background 180ms ease;
}

.toggle-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--white);
  box-shadow:
    0 3px 8px rgba(172, 15, 23, 0.18),
    inset 0 0 0 1px rgba(215, 25, 32, 0.08);
  transform: translateX(0);
  transition: transform 180ms ease;
}

.toggle-input:checked + .toggle-track {
  background: var(--red);
}

.toggle-input:checked + .toggle-track .toggle-thumb {
  transform: translateX(22px);
}

.toggle-input:focus-visible + .toggle-track {
  outline: 2px solid rgba(215, 25, 32, 0.45);
  outline-offset: 3px;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
}

.status-label {
  font-family: var(--mono-font);
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
}

.status-pill {
  padding: 0.36rem 0.7rem;
  border-radius: 999px;
  background: rgba(215, 25, 32, 0.1);
  color: var(--red-dark);
  font-family: var(--mono-font);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

body[data-enabled="false"] .status-pill {
  background: #f4f4f4;
  color: var(--text);
}

.scope-card {
  padding-top: 12px;
}

.scope-title {
  margin: 0 0 10px;
}

.scope-list {
  margin: 0;
  padding-left: 18px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.55;
}

.scope-list li + li {
  margin-top: 6px;
}
```

### `popup.js`

```js
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
```

## Why Each File Exists
- `manifest.json`: declares MV3 entry points, popup, permissions, and YouTube-only content script injection.
- `content.js`: intercepts supported clicks and sends the runtime message.
- `service-worker.js`: opens the new tab and validates the request payload.
- `service-worker.js`: opens the new tab immediately beside the current tab and validates the request payload.
- `popup.html`, `popup.css`, `popup.js`: expose the global on or off toggle.
- `icons/*`: provide a simple red `Y` icon on a white or transparent base for the toolbar and extension metadata.

## Load as an Unpacked Extension
1. Open `chrome://extensions`.
2. Turn on Developer mode.
3. Click **Load unpacked**.
4. Select the repository root folder.
5. Open a `www.youtube.com` page and test a normal video link.

## Manual Smoke Check
1. Open the popup and verify the toggle starts enabled.
2. Left-click a normal YouTube video tile on the home page or search results.
3. Confirm the video opens in a new active tab.
4. Confirm the original page stays on the same feed or results view.
5. Disable the toggle and repeat.
6. Confirm native YouTube navigation returns.

## Future Extension Ideas
- Add a background-tab preference
- Add Shorts support
- Show enabled state with a badge or dynamic icon
- Expand host coverage to `music.youtube.com` or `m.youtube.com` if needed

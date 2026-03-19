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
  if (!extensionEnabled || !shouldInterceptClick(event)) {
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

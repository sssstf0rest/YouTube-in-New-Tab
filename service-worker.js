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

# Research: Chrome MV3 Approach for YouTube-in-New-Tab

## Goal
Build a Chrome extension that turns a plain left-click on a YouTube video link into "open in a new tab" while leaving the current YouTube page in place.

## Research Date
- 2026-03-19

## Key Findings

### 1. `chrome.tabs` belongs in the service worker, not the content script
- Chrome’s official Tabs API reference states that `chrome.tabs` is available to the extension service worker and extension pages, but not to content scripts.
- The same reference also notes that creating tabs is one of the Tabs API features that does not require the `"tabs"` permission.
- Practical result: the content script should detect the click and then ask the service worker to open the tab.
- Source: [chrome.tabs](https://developer.chrome.com/docs/extensions/reference/api/tabs)

### 2. A static YouTube-only content script is the simplest MV3 injection model
- Chrome’s content script documentation recommends static `content_scripts` declarations when the extension should always run on a known host.
- Static content scripts also support `run_at: "document_start"`, which is useful here because the extension needs to intercept clicks before YouTube’s own SPA handlers replace the page.
- Practical result: use a static content script for `https://www.youtube.com/*` and attach one capturing listener on `document`.
- Source: [Content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts)

### 3. One-time runtime messaging is the correct bridge
- Chrome’s message-passing documentation describes `chrome.runtime.sendMessage()` as the standard one-shot communication path between a content script and the extension service worker.
- Practical result: the content script can send `{ type: "OPEN_VIDEO_TAB", url }` and the service worker can reply with a small debug result.
- Source: [Message passing](https://developer.chrome.com/docs/extensions/develop/concepts/messaging)

### 4. `chrome.storage.sync` fits the enable or disable setting
- Chrome’s storage documentation positions `storage.sync` as the settings-friendly storage area that can follow the user’s signed-in Chrome profile.
- Practical result: store a single `enabled` boolean in `chrome.storage.sync`, read it from both popup and content script, and watch `chrome.storage.onChanged` for live updates.
- Source: [chrome.storage](https://developer.chrome.com/docs/extensions/reference/api/storage)

### 5. A popup is the lightest UI surface for the toggle
- Chrome’s action and popup documentation supports registering a toolbar action with a `default_popup` HTML file.
- Practical result: a minimal popup is enough for v1. There is no need for a full options page yet.
- Sources: [Implement an action](https://developer.chrome.com/docs/extensions/develop/ui/implement-action), [Add a popup](https://developer.chrome.com/docs/extensions/develop/ui/add-popup)

### 6. DOM event APIs support a delegated click interceptor
- MDN documents the core DOM behavior needed for this feature:
  - `MouseEvent.button` distinguishes primary-button clicks.
  - `Event.preventDefault()` cancels native link navigation.
  - `Event.stopImmediatePropagation()` stops later listeners from acting on the same event.
  - `Event.composedPath()` helps resolve the clicked element across composed trees.
  - `Element.closest()` finds the surrounding anchor.
  - `addEventListener(..., true)` enables capture-phase interception.
- Practical result: a single capturing `click` listener can resolve the anchor, check that it is a `/watch` URL, and replace the navigation with a new-tab open request.
- Sources:
  - [MouseEvent.button](https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/button)
  - [Event.preventDefault()](https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault)
  - [Event.stopImmediatePropagation()](https://developer.mozilla.org/en-US/docs/Web/API/Event/stopImmediatePropagation)
  - [Event.composedPath()](https://developer.mozilla.org/en-US/docs/Web/API/Event/composedPath)
  - [Element.closest()](https://developer.mozilla.org/en-US/docs/Web/API/Element/closest)
  - [EventTarget.addEventListener()](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener)

## Chosen Method
1. Inject a content script on `https://www.youtube.com/*` at `document_start`.
2. Listen for plain left-clicks during the capture phase.
3. Skip interception entirely when the current page is already a YouTube watch page.
4. Resolve the nearest anchor from the event path.
5. Only continue for same-origin `/watch` URLs that include a `v` query parameter.
6. Cancel the original navigation.
7. Send a runtime message to the service worker.
8. Call `chrome.tabs.create({ url, active: true, windowId, index, openerTabId })` in the service worker so the new tab opens immediately to the right of the current YouTube tab.
9. Keep the current page unchanged.

## Alternatives Considered

### `webRequest`
- Rejected for v1 because this feature is about preserving the current page while opening a separate tab.
- Request interception is the wrong abstraction for this user interaction.
- It would also expand the permission footprint unnecessarily.

### `declarativeNetRequest`
- Rejected for the same reason as `webRequest`.
- Redirect rules can change where the current navigation goes, but they do not model "cancel this click and open a different tab while keeping the current page intact."

### Injecting a script into the page’s main world
- Rejected because the extension can solve the problem from an isolated content script using standard DOM events plus runtime messaging.
- Keeping the logic in the isolated world is safer and simpler.

### MutationObserver plus per-link listeners
- Rejected because YouTube is a SPA with dynamic feed updates.
- Event delegation on `document` is more resilient than attaching listeners to individual tiles or thumbnails.

## Scope Boundaries for v1
- Target host: `https://www.youtube.com/*`
- Supported links: same-origin `/watch?v=...`
- Open behavior: new active tab
- Setting: global `enabled` boolean only
- Watch-page behavior: disabled when the current page is already a YouTube video watch page
- Explicitly out of scope:
  - Opening watch-page recommendations in a new tab
  - Shorts interception
  - Playlist item interception logic
  - Background-tab mode
  - Badge state
  - Mobile YouTube and YouTube Music

## Working Inference
- YouTube’s layout can change frequently, so relying on a single selector like `ytd-thumbnail a` is fragile.
- Delegated event handling with URL validation is the more stable implementation strategy for this extension.

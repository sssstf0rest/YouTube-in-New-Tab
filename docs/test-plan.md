# Test Plan

## Acceptance Criteria
- Plain left-click on a supported YouTube `/watch` link opens the video in a new active tab immediately beside the current tab.
- The current YouTube page remains on the same feed, search results, subscriptions, or channel-video surface.
- Disabled mode restores native YouTube navigation.
- Non-video links are untouched.
- Modifier-click and non-primary-button behaviors are untouched.
- Shorts links are not intercepted in v1.
- If the current page is already a watch page, native same-tab video navigation remains unchanged.
- Popup state changes apply live without reloading the YouTube page.

## Manual Test Matrix

| Scenario | Action | Expected Result |
|----------|--------|-----------------|
| Home feed video tile | Plain left-click a video thumbnail or title | New active tab opens immediately to the right of the current tab; home feed stays in place |
| Search results | Plain left-click a result | New active tab opens immediately to the right of the current tab; search results page stays in place |
| Subscriptions feed | Plain left-click a video | New active tab opens immediately to the right of the current tab; subscriptions list stays in place |
| Channel videos grid | Plain left-click a video card | New active tab opens immediately to the right of the current tab; channel page stays in place |
| Current page is a watch page | Plain left-click a recommended video on the sidebar | Native same-tab navigation occurs; the extension does not open a new tab |
| Disabled mode | Turn popup toggle off, then plain left-click a video | Current page navigates normally inside the same tab |
| Channel avatar or channel name | Plain left-click | Native channel navigation remains unchanged |
| Playlist link | Plain left-click | Native behavior remains unchanged |
| Shorts link | Plain left-click | Native behavior remains unchanged |
| `Cmd`-click or `Ctrl`-click | Modifier-click a video link | Native browser new-tab behavior remains unchanged |
| `Shift`-click | Shift-click a video link | Native behavior remains unchanged |
| Middle-click | Mouse-wheel click a video link | Native behavior remains unchanged |
| Right-click | Open context menu on a video link | Context menu behavior remains unchanged |
| Live popup update | Toggle setting while a YouTube page is already open | Interception behavior changes immediately without page reload |

## Suggested Test URLs
- `https://www.youtube.com/`
- `https://www.youtube.com/results?search_query=openai`
- `https://www.youtube.com/feed/subscriptions`
- Any channel `Videos` tab
- Any watch page with sidebar recommendations

## Debug Workflow

### Extension load or manifest issues
1. Open `chrome://extensions`.
2. Enable Developer mode.
3. Reload the unpacked extension.
4. Check the extension card for manifest or script-load errors.

### Service worker issues
1. Open `chrome://extensions`.
2. On the extension card, open the service worker inspector.
3. Check whether `OPEN_VIDEO_TAB` messages arrive.
4. Confirm `chrome.tabs.create()` succeeds or inspect the logged error.

### Content script issues
1. Open YouTube.
2. Open page DevTools.
3. Check the console for content script errors from `content.js`.
4. Confirm the clicked link resolves to a same-origin `/watch` URL with a `v` parameter.

### Popup issues
1. Open the popup.
2. Toggle the switch.
3. Confirm `chrome.storage.sync` updates.
4. Return to the existing YouTube tab and retest without reloading.

## Common Failure Modes

### A click does nothing
- Likely causes:
  - runtime messaging failed
  - the link was intercepted but the service worker was unavailable
  - the link was not a supported `/watch` URL
- Expected fallback in this scaffold:
  - if the message fails after interception, `content.js` navigates the current tab to avoid a dead click

### A click still navigates in the current tab while enabled
- Likely causes:
  - the link is out of scope
  - the current page is already a YouTube watch page, where interception is intentionally disabled
  - the content script did not load on the page
  - the page interaction used a modifier key or non-primary mouse button

### Popup toggle changes do not apply live
- Likely causes:
  - popup wrote a bad storage value
  - `chrome.storage.onChanged` did not fire in the content script
  - the content script was not injected on that tab

## Regression Checklist
- [ ] Home feed still scrolls and behaves normally
- [ ] Search filters and navigation controls still work
- [ ] Watch-page recommendation clicks remain native same-tab navigation
- [ ] Channel navigation still works
- [ ] Browser native tab shortcuts remain unchanged

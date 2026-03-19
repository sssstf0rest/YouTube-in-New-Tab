# YouTube in New Tab

A lightweight Chrome extension that opens supported YouTube video links in a new adjacent tab instead of replacing the current page.

## Features

- **Open in adjacent tab** — Left-click a supported YouTube video link and open it in a new tab right beside the current tab.
- **On/Off toggle** — Click the extension icon in the toolbar to enable or disable with a single switch.
- **Smart behavior** — Works on YouTube browsing surfaces like Home, Search, Subscriptions, and channel video grids.
- **Watch-page safe** — When the current page is already a YouTube video watch page, the extension does not intercept clicks and normal same-tab navigation is preserved.
- **Minimal footprint** — No analytics, no tracking, no external requests. Just a content script, a service worker, and a small popup.

## Install from Chrome Web Store

> Coming soon

## Install (Development)

1. Clone or download this repository.
2. Open `chrome://extensions` in Chrome.
3. Enable **Developer mode**.
4. Click **Load unpacked** and select the project folder.
5. Open YouTube and reload any already-open YouTube tabs so the content script activates.

## How It Works

1. A content script is injected into `https://www.youtube.com/*`.
2. It listens for capture-phase `click` events.
3. On a plain left-click:
   - If the extension is disabled — **skip**.
   - If the current page is already a YouTube watch page — **skip**.
   - If the click is on an unsupported or non-video link — **skip**.
   - If the click uses modifier keys or already targets `_blank` — **skip**.
   - Otherwise — send an `OPEN_VIDEO_TAB` message to the service worker.
4. The service worker calls `chrome.tabs.create()` and inserts the new tab immediately to the right of the current tab.

## Project Structure

```text
manifest.json                — Extension manifest (Manifest V3)
service-worker.js            — Background service worker: opens the new adjacent tab
content.js                   — Content script: detects supported YouTube video-link clicks
popup.html                   — Toolbar popup with on/off toggle
popup.js                     — Popup logic: reads/writes enabled state
popup.css                    — Popup styling
icons/                       — Extension icons
docs/                        — Architecture, implementation notes, privacy policy, and store docs
store-assets/                — Current Chrome Web Store asset pack
```

## Permissions

| Permission | Why |
|---|---|
| `storage` | Save the on/off toggle preference |
| YouTube page access via `content_scripts.matches` | Detect supported video-link clicks on `https://www.youtube.com/*` |

No data is collected or transmitted. See the full [Privacy Policy](./docs/privacy-policy.html).

## Known Limitations

- **Only works on `www.youtube.com`** — It does not target `m.youtube.com`, `music.youtube.com`, or other sites.
- **Only standard `/watch` links are changed** — Shorts, playlists, channel navigation, and other non-watch links keep their normal behavior.
- **Does not intercept on watch pages** — If the current page is already a video watch page, the extension intentionally stays out of the way.
- **Does not work on Chrome internal pages** — Chrome blocks extension content scripts on pages like `chrome://*` and the Chrome Web Store.
- **Newly installed** — Already-open YouTube tabs need a reload for the content script to activate.

## Documentation

- [Architecture](./docs/architecture.md)
- [Implementation Guide](./docs/implementation.md)
- [Research Notes](./docs/research.md)
- [Test Plan](./docs/test-plan.md)
- [Chrome Web Store Submission Guide](./docs/chrome-web-store-submission.md)
- [Privacy Policy](./docs/privacy-policy.html)

## License

MIT

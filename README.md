# YouTube in New Tab

YouTube in New Tab is a Chrome extension that opens supported YouTube video links in a new adjacent tab instead of replacing the current page.

It is designed for browsing surfaces like Home, Search, Subscriptions, and channel video grids, where you want to keep your current page in place while opening the next video.

## What It Does

- Opens standard YouTube `/watch` links in a new active tab beside the current tab
- Keeps the current YouTube page in place on feed, search, subscriptions, and channel pages
- Includes a simple popup toggle to enable or disable the behavior
- Stores only a single on/off setting with `chrome.storage.sync`

## Important Behavior

- The extension runs only on `https://www.youtube.com/*`
- It only targets standard `/watch?v=...` video links
- It preserves normal browser behavior for `Ctrl`/`Cmd` click, `Shift` click, middle click, and right click
- It does not intercept Shorts, playlists, channel navigation, or other non-watch links
- If the current page is already a YouTube watch page, the extension does not intercept clicks and normal same-tab video navigation is preserved

## Why This Exists

On YouTube, a normal left-click usually replaces the current tab. This extension changes that behavior for supported pages so you can keep browsing without losing your place.

## Tech Stack

- Chrome Extension Manifest V3
- Content script for YouTube page click interception
- Service worker for `chrome.tabs.create()`
- Popup UI with a single enable or disable switch
- Plain HTML, CSS, and JavaScript with no build step for the extension itself

## Permissions

The extension uses:

- `storage`
  Used only to save the user's on/off preference.

It does not request broad extra permissions such as `tabs`, `webRequest`, or `declarativeNetRequest`.

## Install Locally

1. Open `chrome://extensions`
2. Turn on Developer mode
3. Click `Load unpacked`
4. Select this repository folder
5. Open YouTube and test a standard video link from Home, Search, Subscriptions, or a channel page

## Project Structure

```text
.
├── manifest.json
├── service-worker.js
├── content.js
├── popup.html
├── popup.css
├── popup.js
├── icons/
├── docs/
│   ├── architecture.md
│   ├── chrome-web-store-submission.md
│   ├── implementation.md
│   ├── privacy-policy.html
│   ├── research.md
│   ├── tasks.md
│   └── test-plan.md
├── store-assets/
└── README.md
```

## Documentation

- Architecture: [docs/architecture.md](./docs/architecture.md)
- Implementation details: [docs/implementation.md](./docs/implementation.md)
- Research notes: [docs/research.md](./docs/research.md)
- Test plan: [docs/test-plan.md](./docs/test-plan.md)
- Chrome Web Store submission guide: [docs/chrome-web-store-submission.md](./docs/chrome-web-store-submission.md)
- Privacy policy: [docs/privacy-policy.html](./docs/privacy-policy.html)

## Chrome Web Store Assets

The current canonical store asset pack is in [store-assets](./store-assets/).

Current standard files:

- `design 440 x 280.png`
  Small promo tile
- `design 1440 x 560.png`
  Wide promo graphic file used as the marquee asset source
- `design 1280 x 800.png`
  Store screenshot
- `design 3840 x 2160.png`
  High-resolution master artwork
- `design.pptx`
  Editable source deck

## Privacy

The extension does not use analytics, ads, or a developer-run backend. It stores only a single setting:

```json
{ "enabled": true | false }
```

See the full privacy policy at [docs/privacy-policy.html](./docs/privacy-policy.html).

## Development Notes

- Store-related copy and submission answers are maintained in [docs/chrome-web-store-submission.md](./docs/chrome-web-store-submission.md)
- The current manually prepared files inside `store-assets/` are the standard assets for publication
- If you change user-facing behavior, update both the extension files and the docs before publishing

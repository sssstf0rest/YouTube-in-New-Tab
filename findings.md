# Findings & Decisions

## Requirements
- Build a Chrome extension that opens YouTube videos in a new tab instead of replacing the current page on plain left-click.
- Research current Chrome extension and browser API constraints online before implementing.
- Write down methods, ideas, full implementation code, and task breakdown as markdown files in `docs/`.
- Include a basic on/off control.
- Keep v1 focused on desktop Chrome, `www.youtube.com`, and normal `/watch` links.

## Research Findings
- Chrome’s official `chrome.tabs` docs state the Tabs API can be used by the service worker and extension pages, but not content scripts.
- Chrome’s official `chrome.tabs` docs also state creating a tab does not require the `"tabs"` permission, which keeps the manifest smaller.
- Chrome’s content script docs confirm content scripts can directly use `chrome.storage` and `chrome.runtime.sendMessage()`.
- Chrome’s content script docs confirm static `content_scripts` can be scoped to `https://www.youtube.com/*` and configured with `run_at: "document_start"`.
- Chrome’s message-passing docs confirm one-time `chrome.runtime.sendMessage()` is the correct bridge between a content script and service worker.
- Chrome’s storage docs recommend `storage.sync` for settings that should follow the user’s browser profile.
- MDN documents `preventDefault()`, `stopImmediatePropagation()`, `composedPath()`, `closest()`, and `MouseEvent.button`, which together support a robust delegated click interceptor.
- Chrome Web Store image guidance currently requires a `128x128` icon, a `440x280` small promo tile, and at least one screenshot at `1280x800` or `640x400`.
- Chrome Web Store privacy guidance currently requires a single purpose statement, a privacy policy URL, data usage disclosures, and limited-use certification before publication or update.
- Chrome’s user-data FAQ states that products handling sensitive user data still need a privacy policy even when the data is only stored locally or in `chrome.storage.sync`.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Intercept clicks rather than redirecting requests | The requirement is to preserve the current page and open a separate tab, which request-redirection APIs do not model well. |
| Match only same-origin `/watch` URLs with a `v` parameter | Keeps v1 narrow and avoids surprising behavior on Shorts, channels, playlists, and navigation chrome. |
| Keep a cached `enabled` state in the content script and update via `chrome.storage.onChanged` | Allows popup changes to take effect immediately without reloading YouTube. |
| Revalidate the URL in the service worker before opening a tab | Defense-in-depth for any incoming runtime message. |
| Use plain HTML/CSS/JS with no build tooling | Fastest path for a greenfield repo and easiest to inspect in docs. |
| Generate Chrome Web Store assets locally with Pillow | Produces a repeatable red-and-white asset pack without depending on external design tools. |
| Recommend conservative privacy disclosure for submission | The extension handles YouTube click interactions and clicked watch URLs to provide its single purpose, so conservative disclosure reduces review risk. |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Direct browser automation to inspect YouTube was blocked by a profile conflict in the DevTools MCP browser | Proceeded with official Chrome docs, MDN references, and code designed for delegated DOM interception on SPA pages. |

## Resources
- Chrome content scripts: https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts
- Chrome message passing: https://developer.chrome.com/docs/extensions/develop/concepts/messaging
- Chrome tabs API: https://developer.chrome.com/docs/extensions/reference/api/tabs
- Chrome storage API: https://developer.chrome.com/docs/extensions/reference/api/storage
- Chrome implement action: https://developer.chrome.com/docs/extensions/develop/ui/implement-action
- Chrome add popup: https://developer.chrome.com/docs/extensions/develop/ui/add-popup
- Chrome debugging extensions: https://developer.chrome.com/docs/extensions/mv2/tutorials/debugging
- Chrome Web Store images: https://developer.chrome.com/docs/webstore/images
- Chrome Web Store listing fields: https://developer.chrome.com/docs/webstore/cws-dashboard-listing/
- Chrome Web Store privacy fields: https://developer.chrome.com/docs/webstore/cws-dashboard-privacy
- Chrome Web Store privacy policy guidance: https://developer.chrome.com/docs/webstore/program-policies/privacy
- Chrome Web Store limited use guidance: https://developer.chrome.com/docs/webstore/program-policies/limited-use
- Chrome Web Store user data FAQ: https://developer.chrome.com/docs/webstore/program-policies/user-data-faq
- MDN `preventDefault()`: https://developer.mozilla.org/en-US/docs/Web/API/Event/preventDefault
- MDN `stopImmediatePropagation()`: https://developer.mozilla.org/en-US/docs/Web/API/Event/stopImmediatePropagation
- MDN `composedPath()`: https://developer.mozilla.org/en-US/docs/Web/API/Event/composedPath
- MDN `closest()`: https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
- MDN `MouseEvent.button`: https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/button
- MDN `addEventListener()`: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener

## Visual/Browser Findings
- The repo was effectively empty except for `.git`, `.DS_Store`, and an empty `docs/` directory.
- The planned extension should therefore define both the implementation scaffold and the docs structure from scratch.
- The feature relies on event delegation rather than any fixed YouTube DOM selector, which makes it resilient to feed and recommendation layout changes.

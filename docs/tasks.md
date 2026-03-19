# Tasks

## Completed in This Pass
- [x] Research current Chrome MV3 extension constraints and relevant DOM APIs
- [x] Decide on the MV3 content-script plus service-worker architecture
- [x] Create a working extension scaffold in the repo root
- [x] Add a popup-based enable or disable toggle using `chrome.storage.sync`
- [x] Simplify the popup to a compact red-and-white switch layout
- [x] Add a simple red `Y` icon set for the extension
- [x] Write the research notes in `docs/research.md`
- [x] Write the architecture spec in `docs/architecture.md`
- [x] Write copy-paste-ready implementation code in `docs/implementation.md`
- [x] Write a manual QA plan in `docs/test-plan.md`

## Remaining Validation Work
- [ ] Load the extension in Chrome as unpacked
- [ ] Verify feed page behavior on Home
- [ ] Verify search results behavior
- [ ] Verify Subscriptions behavior
- [ ] Verify channel video-grid behavior
- [ ] Verify watch pages are intentionally not intercepted
- [ ] Verify disabled mode restores native navigation
- [ ] Verify `Cmd`-click, `Ctrl`-click, `Shift`-click, middle-click, and right-click remain unchanged
- [ ] Verify Shorts links are not intercepted
- [ ] Verify popup changes apply without reloading YouTube

## Hardening Tasks
- [ ] Add small, controlled debug logging behind a flag if manual QA exposes ambiguity
- [ ] Consider a tiny automated test harness for URL-matching helpers
- [x] Add icons before packaging or publishing
- [x] Add `.gitignore` rules if the repo will be committed from this machine

## Optional Future Features
- [ ] Background-tab mode
- [ ] Shorts support
- [ ] Playlist-entry handling
- [ ] Badge state or icon state
- [ ] Per-site or per-surface settings
- [ ] Support for `music.youtube.com`

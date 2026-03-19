# Task Plan: Youtube-in-New-Tab Research, Docs, and MV3 Scaffold

## Goal
Create a researched, documented, and working Manifest V3 Chrome extension scaffold that opens YouTube `/watch` links in a new tab on plain left-click, with complete markdown documentation in `docs/`.

## Current Phase
Phase 5

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints and requirements
- [x] Document findings in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Define technical approach
- [x] Create project structure if needed
- [x] Document decisions with rationale
- **Status:** complete

### Phase 3: Implementation
- [x] Execute the plan step by step
- [x] Write code to files before executing
- [x] Test incrementally
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Verify all requirements met
- [x] Document test results in progress.md
- [x] Fix any issues found
- **Status:** complete

### Phase 5: Delivery
- [x] Review all output files
- [x] Ensure deliverables are complete
- [x] Deliver to user
- **Status:** complete

## Key Questions
1. Which Chrome extension architecture fits the requirement without over-permissioning?
2. Which YouTube interactions should v1 intercept without breaking native browser behaviors?
3. How should the repo store both implementation details and research findings for later iteration?

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use Manifest V3 with a service worker | Current Chrome extension standard and required for a new extension. |
| Use a static YouTube-only content script at `document_start` | Earliest reliable hook for intercepting YouTube SPA clicks before native handlers run. |
| Send `{ type: "OPEN_VIDEO_TAB", url }` from content script to service worker | `chrome.tabs` is available in the service worker but not in content scripts. |
| Store `{ enabled: boolean }` in `chrome.storage.sync` | Small global preference, sync-friendly, and accessible from popup plus content script. |
| Ship a toolbar popup with a single toggle | Minimal UX that satisfies the user’s requested on/off control without adding an options page. |
| Create the real extension scaffold in addition to docs | Keeps the markdown code examples aligned with working files in the repo. |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| Chrome DevTools MCP profile conflict prevented live YouTube DOM inspection | 1 | Switched to official documentation and web research rather than blocking on browser automation. |
| None during local syntax and manifest validation | 1 | `json.tool` and `node --check` both passed. |

## Notes
- Re-read this plan before major decisions.
- Update findings.md after research or discovery.
- Keep the docs aligned with the actual scaffold files.

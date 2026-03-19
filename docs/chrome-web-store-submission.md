# Chrome Web Store Submission Guide

This file gives you the current asset checklist, draft listing copy, and recommended answers for the Chrome Web Store submission flow for **YouTube in New Tab**.

## Official Sources Used
- [Supplying Images](https://developer.chrome.com/docs/webstore/images)
- [Complete your listing information](https://developer.chrome.com/docs/webstore/cws-dashboard-listing/)
- [Fill out the privacy fields](https://developer.chrome.com/docs/webstore/cws-dashboard-privacy)
- [Privacy Policies](https://developer.chrome.com/docs/webstore/program-policies/privacy)
- [Limited Use](https://developer.chrome.com/docs/webstore/program-policies/limited-use)
- [Updated Privacy Policy & Secure Handling Requirements FAQ](https://developer.chrome.com/docs/webstore/program-policies/user-data-faq)
- [Listing Requirements](https://developer.chrome.com/docs/webstore/program-policies/listing-requirements)
- [Configure extension icons](https://developer.chrome.com/docs/extensions/develop/ui/configure-icons)
- [Register your developer account](https://developer.chrome.com/docs/webstore/register/)

## What Is Required Right Now
- Google’s current image guidance says the required images are:
  - one `128x128` PNG extension icon
  - one `440x280` small promo tile
  - at least one screenshot at `1280x800` or `640x400`
- The same guidance says the marquee promo image is optional but recommended if you want stronger featuring opportunities.
- The listing page guidance says the Store listing tab also asks for a detailed description, category, language, and optional URLs.
- The Privacy tab asks for a single purpose statement, permission justifications, remote code declaration, privacy policy URL, and data usage disclosures.

## Asset Files To Upload

### Icon
- Use: [icons/icon-128.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/icons/icon-128.png)

### Small promo tile
- Use: [store-assets/promo-small-440x280.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/promo-small-440x280.png)

### Marquee promo tile
- Optional but recommended: [store-assets/promo-marquee-1400x560.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/promo-marquee-1400x560.png)

### Screenshots
- [store-assets/screenshots/screenshot-01-search-results.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/screenshots/screenshot-01-search-results.png)
- [store-assets/screenshots/screenshot-02-home-feed.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/screenshots/screenshot-02-home-feed.png)
- [store-assets/screenshots/screenshot-03-popup-enabled.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/screenshots/screenshot-03-popup-enabled.png)
- [store-assets/screenshots/screenshot-04-watch-page.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/screenshots/screenshot-04-watch-page.png)
- [store-assets/screenshots/screenshot-05-popup-disabled.png](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/store-assets/screenshots/screenshot-05-popup-disabled.png)

## Suggested Answers For The Store Listing Tab

### Name
- `YouTube in New Tab`

### Short description
- `Open YouTube video watch links in a new tab on plain left-click.`

### Detailed description
Use this:

```text
Keep your place on YouTube while opening videos in a separate tab.

YouTube in New Tab changes standard YouTube watch-link clicks so videos open in a new tab immediately beside your current tab instead of replacing the page you are on.

This is useful when you are browsing Home, Search, Subscriptions, Channel pages, or watch-page recommendations and want to keep your current view in place while opening the next video.

Features:
- Opens standard YouTube /watch links in a new adjacent tab
- Keeps your current YouTube page in place
- Works with Home, Search, Subscriptions, channel video grids, and recommendations
- Includes a simple popup switch to turn the feature on or off instantly
- Uses only the minimum storage permission needed to save the on/off preference

Scope:
- Targets www.youtube.com
- Changes standard /watch link behavior only
- Leaves Shorts, playlists, channels, and normal modifier-click behavior untouched

No ads. No analytics. No developer-run backend.
```

### Category
- `Productivity`

### Language
- `English`

### Mature content
- `No`

### Promo video
- `Leave blank for now`
- Optional only. Add one later if you record a short feature demo.

### Homepage URL
- Recommended: `https://github.com/sssstf0rest/Youtube-in-New-Tab`

### Support URL
- Recommended: `https://github.com/sssstf0rest/Youtube-in-New-Tab/issues`

### Official URL
- `Leave blank unless you verify a site in Search Console`
- If you later enable GitHub Pages or use your own domain, use that verified site here.

## Suggested Screenshot Order
1. `screenshot-01-search-results.png`
2. `screenshot-02-home-feed.png`
3. `screenshot-03-popup-enabled.png`
4. `screenshot-04-watch-page.png`
5. `screenshot-05-popup-disabled.png`

## Suggested Answers For The Privacy Tab

### Single purpose description
- `Open supported YouTube watch links in a new tab beside the current tab so users can keep their current YouTube page in place.`

### Permission justification
- `storage`: `Stores the user's on/off preference and syncs that preference across Chrome browsers when Chrome Sync is enabled.`

### Remote code
- `No, I am not using remote code.`

### Privacy policy URL
- You must host the existing privacy policy publicly over HTTPS.
- If you publish it with GitHub Pages, a likely URL is:
  - `https://sssstf0rest.github.io/Youtube-in-New-Tab/PrivacyPolicy/`
- Do not paste a local file path into the dashboard.

### Data usage disclosure
Recommended conservative selection:

- Select these data types as collected:
  - `Website content`
  - `User activity`
- Rationale:
  - the extension reads clicked YouTube watch-link URLs and YouTube click interactions to provide its only feature
  - processing stays local to the extension
  - the extension does not transmit this data to your own servers or third parties

### Limited use certifications
Check the certifications that state the data:
- is used only to provide or improve the item’s single purpose
- is not sold to third parties
- is not used or transferred for purposes unrelated to the item’s single purpose
- is not used or transferred to determine creditworthiness or for lending purposes
- is not used for personalized ads

## Suggested Answers For Distribution
- Pricing: `Free`
- Visibility: `Public`
- Regions: `All regions` unless you intentionally want to limit distribution

## Suggested Answers For Test Instructions
- `No login, credentials, payment, or special environment required.`
- `Load the unpacked extension, open https://www.youtube.com/ or a YouTube results page, and left-click a standard /watch video link.`
- `Expected result: the video opens in a new active tab immediately beside the current tab, and the original YouTube page stays in place.`
- `Open the extension popup and switch it off to verify native YouTube navigation returns.`

## Developer Account / Registration Blanks You Still Need To Fill Yourself
- Developer account email: use an email you actively monitor
- Support email: replace the placeholder in the privacy policy and use the same contact in your listing
- Publisher name: choose the public name you want shown under the listing
- Official URL: only if you verify a site

## Important Remaining Publishing Tasks
- Replace the contact placeholder in [PrivacyPolicy/index.html](/Users/sssst/Files/Workspace/Repos/YouTube-in-New-Tab/PrivacyPolicy/index.html)
- Host the privacy policy at a public HTTPS URL
- Package the extension ZIP for upload
- Manually verify the screenshots against the final extension build before submission

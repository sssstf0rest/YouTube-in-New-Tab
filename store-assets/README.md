# Chrome Web Store Asset Pack

This folder contains the generated asset pack for the Chrome Web Store listing.

## Required assets
- `../icons/icon-128.png`
- `promo-small-440x280.png`
- `screenshots/screenshot-01-search-results.png`

## Recommended assets included here
- `promo-marquee-1400x560.png`
- `screenshots/screenshot-02-home-feed.png`
- `screenshots/screenshot-03-popup-enabled.png`
- `screenshots/screenshot-04-watch-page.png`
- `screenshots/screenshot-05-popup-disabled.png`

## Official sizing used
- Store icon: `128x128` PNG
- Small promo tile: `440x280`
- Marquee promo tile: `1400x560`
- Screenshots: `1280x800`

## Regeneration
Run:

```bash
python3 scripts/generate_store_assets.py
```

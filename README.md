# Paisajes Coloniales - Static Site Archive

This is the archived static site version of **Paisajes Coloniales** (Colonial Landscapes), a digital humanities project mapping colonial territories in 17th-century Andean regions.

## Overview

This repository contains a **static HTML site** that was originally built with Jekyll/Wax but has been converted to a pure static archive for long-term preservation and maintainability.

**Live site:** https://www.paisajescoloniales.com

## Project Structure

```
spanish/
├── *.html                    # Main pages (index, historia, explora, coleccion, etc.)
├── paisajes/                 # Object detail pages (obj1.html - obj59.html)
├── assets/
│   ├── css/
│   │   └── main.css         # Main stylesheet (compiled from SCSS)
│   ├── js/
│   │   ├── gallery.js       # Gallery filtering logic
│   │   ├── modals.js        # Modal z-index management
│   │   ├── object-viewer.js # Leaflet IIIF image viewer
│   │   └── scroll-handler.js # GSAP ScrollTrigger for card stacking
│   ├── bootstrap/           # Bootstrap 4 (self-hosted)
│   ├── jquery/              # jQuery 3.5.1 (self-hosted)
│   ├── popper.js/           # Popper.js (self-hosted)
│   └── img/                 # Images and IIIF derivatives
├── scripts/
│   └── generate_iiif.py     # IIIF tile generator
└── README.md                # This file
```

## Key Features

### 1. Historia (Story Mode)
- **Card stacking navigation** powered by GSAP ScrollTrigger
- Sequential panels that pin as you scroll
- 38 Bootstrap modals with historical content
- 8 image carousels

### 2. Explora (Explore)
- Interactive map interface
- 23 modal popups with regional information

### 3. Colección (Collection)
- **Filterable gallery** with 46 objects
- Vanilla JavaScript filtering by category
- Fade animations

### 4. Object Viewers
- 59 individual object pages
- **Leaflet-based IIIF image viewer** for zoomable high-resolution images
- Self-hosted IIIF tiles (no external dependencies)

## Technology Stack

### Self-Hosted Components
- **Bootstrap 4.5.3** - UI framework
- **jQuery 3.5.1** - Required for Bootstrap modals/carousels
- **Popper.js** - Required for Bootstrap tooltips/popovers
- **Leaflet 1.7.1** - Map library for IIIF viewers
- **leaflet-iiif** - IIIF plugin for Leaflet
- **GSAP 3.11.3** - Animation library for card stacking
- **Normalize.css 5.0.0** - CSS reset
- **GreenSock CSS** - GSAP demo styles

### CDN Dependencies
The following remain on CDN:

1. **Google Fonts**
   - Lora (serif, body text)
   - Raleway (sans-serif, headings)
   - Material Icons

2. **Google Analytics** - Site analytics

## Maintenance Guide

### Updating IIIF Images

If you add new images or modify existing ones:

```bash
# Regenerate IIIF tiles for production
python3 scripts/generate_iiif.py --base-url https://paisajescoloniales.com

# Or for local testing
python3 scripts/generate_iiif.py --base-url http://127.0.0.1:8001
```

### Local Testing

Since there's no build process, you can test with any static server:

```bash
# Python
python3 -m http.server 8001

# Or if you have Jekyll (not required)
bundle exec jekyll serve --port 8001 --skip-initial-build
```

**Important:** When testing locally, regenerate IIIF tiles with the local URL first, otherwise images won't load.

### File Organization

- **DO NOT** delete or rename files in `paisajes/` - these are referenced by the collection
- Object IDs match filenames: `obj1.html` = object ID "obj1"
- Some objects have multiple pages (e.g., obj27_1, obj27_2) - only first page is linked

### JavaScript Dependencies

**Files with jQuery** (Bootstrap components):
- `historia.html` - 38 modals, 8 carousels
- `explora.html` - 23 modals

**Files with vanilla JS only:**
- `coleccion.html` - Gallery filtering
- `paisajes/*.html` - Pagination links

**All pages use:**
- `object-viewer.js` (if IIIF viewer present)
- `gallery.js` (if gallery present)
- `modals.js` (if modals present)
- `scroll-handler.js` (historia.html only - GSAP card stacking)

## Archive History

This site was archived and refactored in 2024-2025 with the following goals:

1. **Remove build dependencies** - Converted from Jekyll/Wax to pure static HTML
2. **Eliminate code duplication** - Extracted JavaScript into reusable modules
3. **Remove dead code** - Deleted 549KB of unused Bootstrap SCSS, source maps, etc.
4. **Modernize JavaScript** - Converted jQuery to vanilla JS where possible
5. **Self-host critical dependencies** - Bootstrap, jQuery, Leaflet now local

### What Changed

**Removed:**
- UniversalViewer (CDN references, never actually used)
- Unused scripts (script.js, st-script.js, 296KB unused)
- Bootstrap source SCSS (253KB, site uses compiled CSS)
- CSS source maps (not needed for static site)
- Duplicate inline JavaScript (extracted to modules)

**Converted to vanilla JS:**
- Gallery filtering (event delegation pattern)
- Modal z-index management
- Object viewer pagination links
- General DOM manipulation

**Kept with jQuery:**
- Bootstrap modals (Bootstrap 4 requires jQuery)
- Bootstrap carousels (Bootstrap 4 requires jQuery)

**Kept with GSAP:**
- Card stacking in historia.html (complex pinning behavior, tried vanilla JS but GSAP works better)

### Code Reduction

- **~2,184 lines** of duplicate JavaScript eliminated
- **549KB** of dead code removed
- **59 files** refactored (all object pages)

## Browser Compatibility

Tested and working in:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

Requires JavaScript enabled for:
- Gallery filtering
- Image viewers
- Modals
- Card stacking navigation

## License

Content and code belong to the Paisajes Coloniales project.

## Contact

For questions about this archive or the original project, contact the project maintainer.

---

**Last updated:** January 2025
**Archive version:** Static HTML (post-Jekyll)

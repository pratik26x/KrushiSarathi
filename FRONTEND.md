# KrushiSarathi — Frontend Architecture & Animation Guide

This document describes how the web frontend is built, which libraries are used, and how motion and animations work across the project.

---

## 1. Overall stack

| Layer | Technology |
|--------|------------|
| **Server** | Python **Flask** renders HTML (no separate React/Vue SPA). |
| **Templating** | **Jinja2** (`templates/*.html`): `{{ }}`, `{% %}`, `url_for()`, `session`. |
| **Structure** | Semantic HTML5 sections, divs, nav, footer. |
| **Styling** | Plain **CSS** per page under `static/css/` (e.g. `style.css`, `soilTesting.css`). |
| **Behavior** | **Vanilla JavaScript** in `static/js/` or inline `<script>` in some templates. |
| **Assets** | Images under `static/images/` (referenced from templates). |

The browser receives **finished HTML** from Flask; there is no client-side router. Each route can use its own CSS file for a consistent but page-specific look.

---

## 2. How pages are “created”

1. User requests a URL (e.g. `/`).
2. Flask runs a view in `app.py` and calls `render_template('index.html', ...)`.
3. Jinja2 fills in dynamic pieces (e.g. `{% if session.logged_in %}`, `{{ url_for('loans') }}`).
4. The response includes `<link>` to CSS and `<script>` tags; the browser loads static files from `/static/...`.

**Key Jinja patterns used:**

- `{{ url_for('static', filename='css/style.css') }}` — correct URL for CSS/JS/images.
- `{{ url_for('home') }}`, `{{ url_for('signup') }}` — links between pages.
- Session-aware UI on the home page (welcome message vs Sign In).

---

## 3. External libraries (CDN)

These are loaded from the network in `templates/index.html` (and similar patterns elsewhere).

| Library | Source | Purpose |
|---------|--------|---------|
| **Boxicons** | `unpkg.com/boxicons` | Icon font (e.g. `bx-menu` hamburger). |
| **Remix Icon** | `jsdelivr` | Additional icon set. |
| **Font Awesome 6** | `cdnjs` | Social icons in footer (`fab fa-facebook-f`, etc.). |
| **Google Translate** | `translate.google.com` | Optional widget (`loadGoogleTranslate`; UI hook is commented out in HTML). |
| **DotLottie Player** | `unpkg.com/@dotlottie/player-component` | Plays **Lottie** / **DotLottie** animations from JSON URLs. |

**Fonts:** `style.css` references **Inter** (Google-style usage in rules); ensure a `<link>` to Google Fonts exists if you rely on Inter loading (add if missing).

No npm/Webpack bundler is required for these; the browser loads scripts and styles directly from CDNs.

---

## 4. Animation systems (how they work)

The project uses **three complementary approaches**.

### 4.1 Lottie / DotLottie (vector animations)

**Where:** `templates/index.html` (hero + financial section).

**What loads:**

```html
<script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
```

**What you put in HTML:**

```html
<dotlottie-player
    src="https://lottie.host/.../....json"
    background="transparent"
    speed="1"
    loop
    autoplay>
</dotlottie-player>
```

**How it works:**

- **Lottie** animations are described as **JSON** (vectors, keyframes, timing).
- **`dotlottie-player`** is a **Web Component** that downloads that JSON and renders it with **Canvas/SVG** in the browser.
- `loop` + `autoplay` start the animation when the page loads; `speed` scales playback.

**Dependencies:** Live internet access to `unpkg.com` and `lottie.host` (or your own hosted `.json`).

---

### 4.2 CSS: transitions, keyframes, hover

**Where:** Primarily `static/css/style.css` (and other page CSS files).

**Examples:**

- **`transition`** on links and buttons (e.g. `transition: all .6s ease`) for smooth color and hover effects.
- **`scroll-behavior: smooth`** on `html` for in-page anchor jumps (`#about-section`).
- **`@keyframes rollDown`** — defines a coin “roll” path (`translateY` + `rotate` + `opacity`). The coin’s motion on the live site is driven mainly by JavaScript (below); `rollDown` is available if you assign it via `animation` on an element.

**How it works:** The browser interpolates property values over time; no JavaScript is required for simple hovers and keyframe animations once CSS is applied.

---

### 4.3 JavaScript-driven scroll animation (home page coin)

**Where:** `static/js/script.js` + `.coin-container` in `style.css`.

**How it works:**

1. On `DOMContentLoaded`, the script selects `.coin-container` and `.Benefits-section`.
2. On **`scroll`**, it reads `benefitsSection.getBoundingClientRect().top` and computes a **scroll progress** value between `0` and `1`.
3. It sets **inline styles** on the coin container:
   - `transform: translateY(...) rotate(...)`
   - `opacity: ...`

So the coin **moves and rotates continuously** as you scroll, tied to how far the “About” section has entered the viewport. This is **imperative** animation (JS updates style each frame event), not the Lottie player.

An older **Intersection Observer** variant is left commented at the top of `script.js`; the active code uses **scroll listeners** instead.

---

### 4.4 Scroll-triggered CSS classes (Soil Testing page)

**Where:** `templates/soilTesting.html` (inline script) + `static/css/soilTesting.css`.

**How it works:**

1. Elements declare intent with attributes like `data-animate="slide-in-left"`.
2. On **`scroll`** (and **`load`**), `animateOnScroll()` runs:
   - Finds all `[data-animate]`.
   - If the element is near the viewport and the user is scrolling **down**, it adds a class matching `data-animate` (e.g. `slide-in-left`).
   - Scrolling **up** can **remove** the class to reverse the effect.
3. CSS defines those classes with **`@keyframes`** (e.g. `slideInLeft`, `slideInRight`, `slideUpScroll`) and sets `animation: ... forwards`.

So animation here is **CSS-based**, but **triggered by JavaScript** toggling classes.

---

## 5. Deep dive: How animations are rendered and used in this project

This section explains **what the browser does** when each animation runs, and **exactly where** it appears in the codebase.

### 5.1 Browser rendering in brief (common to all pages)

When you open a page, the browser roughly does:

1. **Parse HTML** → builds the **DOM** (tree of elements).
2. **Parse CSS** → builds the **CSSOM** (which rules apply to which nodes).
3. **Layout** → computes size and position of every box (“reflow”).
4. **Paint** → fills pixels (text, colors, images, borders).
5. **Composite** → combines layers into the final image on screen.

**Why this matters for animation:**

- Properties like **`transform`** and **`opacity`** are often handled in the **compositor** (GPU-friendly). Updating them many times per second is relatively cheap.
- Changing **`width`**, **`top`**, or **`margin`** often forces **layout** again, which is heavier.
- This project mostly animates **`transform`** / **`opacity`** for motion, which is a good fit for smooth scrolling.

---

### 5.2 DotLottie (`<dotlottie-player>`) — loading, parsing, drawing

**Files:** `templates/index.html` (markup + script tag at bottom).

**Placement in the page (two separate players):**

| Location | Wrapper | `src` host | Approx. role |
|----------|---------|------------|----------------|
| Hero | `.hero-animation` | `lottie.host/.../B27ZuADZd1.json` | Illustration beside headline |
| Financial section | `.lottie-animation` | `lottie.host/.../Jy5bhYcooj.json` | Decorative motion in finance block |

**Load order (important):**

1. The browser parses HTML and sees unknown tags `<dotlottie-player>` — they exist in the DOM as **custom elements** before the script runs.
2. At the **end of `<body>`**, this runs:

   ```html
   <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
   ```

3. Because `type="module"`, the script is **deferred**: it runs after HTML is parsed, then **registers** the custom element with `customElements.define(...)`.
4. The browser **upgrades** each `<dotlottie-player>` in the DOM: the component’s lifecycle (e.g. `connectedCallback`) runs.

**What the component does internally (conceptual):**

1. **Fetch** the animation file from `src` (HTTP GET). The file is **JSON** describing vector shapes, layers, and **keyframes** (property values over time), in Lottie / DotLottie format.
2. **Decode** that data into a runtime model (paths, transforms, easing).
3. Start a **time loop** (typically aligned to **`requestAnimationFrame`**, ~60 fps): each frame, interpolate properties between keyframes for the current time.
4. **Rasterize / draw** the current frame — commonly to a **`<canvas>`** inside the shadow DOM, or to **SVG** nodes, depending on player implementation and animation content.
5. With **`loop`** and **`autoplay`**, when time passes the end of the timeline it **wraps** and keeps going. **`speed="1"`** is normal playback; other values scale time.

**How this differs from CSS animation:**

- Lottie is **script-driven playback** of **vector** data from JSON; the CPU/GPU work is “draw this frame’s vectors.”
- CSS `@keyframes` is **declarative**: the browser’s animation engine interpolates declared CSS properties over time.

**Requirements:** Network access to **unpkg** (for the player script) and **lottie.host** (for the JSON). Offline or blocked CDNs mean the animation does not appear.

---

### 5.3 CSS transitions and keyframes (declarative browser animation)

**Where:** `static/css/style.css`, `static/css/soilTesting.css`, and other page stylesheets.

**Transitions** (`transition: …` on `.navlist a`, buttons, cards):

- When a **hovered** or **focused** state changes a property (e.g. `color`), the browser **interpolates** from old to new over the duration you set.
- No JavaScript is required; the **style engine** schedules intermediate values each frame.

**Keyframes** (`@keyframes name { … }` + `animation: name …`):

- You define **keyframes** at percentages of the animation duration (0%, 100%, etc.).
- The browser computes **in-between** values (easing curves) and applies them over time.
- **`forwards`** keeps the **final** keyframe state after the animation ends (used on Soil Testing slide classes).

**Smooth scrolling:** `html { scroll-behavior: smooth; }` in `style.css` tells the browser to **animate** the scroll position when you follow a link to `#about-section` etc., instead of jumping instantly.

**Unused / alternate path on home:** `@keyframes rollDown` in `style.css` targets the coin metaphorically (translate + rotate + opacity). The **commented** code in `script.js` would have applied `animation: rollDown 5s …` when the section entered view via **Intersection Observer**. The **active** code does **not** use `rollDown`; it uses scroll-driven `transform` instead (see below).

---

### 5.4 JavaScript scroll-linked animation — coin on the home page

**Files:** `static/js/script.js`, markup in `templates/index.html` (`.coin-container` / `.coin` inside `.Benefits-section`), initial styles in `static/css/style.css` (`.coin-container` starts with `opacity: 0`).

**Flow:**

1. **`DOMContentLoaded`** fires → script runs once.
2. It stores references to **`.coin-container`** (the moving wrapper) and **`.Benefits-section`** (the scroll reference).
3. On every **`window` `scroll`** event:
   - **`getBoundingClientRect().top`** on the benefits section gives **distance from the top of the viewport** to that section’s top edge (in pixels).
   - A **progress** value is computed:  
     `scrollProgress = (windowHeight - sectionTop) / windowHeight`, clamped to `[0, 1]`.
   - As you scroll down and the section **moves up** through the viewport, `sectionTop` decreases, so `scrollProgress` **increases** toward 1.
4. The script sets **inline styles** on the coin container:
   - **`transform: translateY(300 * progress px) rotate(360 * progress deg)`** — moves down up to 300px and spins one full turn.
   - **`opacity: scrollProgress`** — fades in as progress increases.

**Rendering path each scroll:**

- Inline `style` changes → **style recalculation** for that element.
- **`transform`** and **`opacity`** updates are typically **composited** without full page relayout.
- The scroll handler can fire **many times per second**; browsers may coalesce paints, but heavy work inside `scroll` should still be kept small (this script only does a few math ops and one style write).

**Contrast with Lottie:** Here **you** control the “frame” via **scroll position**, not time. The motion is **one-to-one** with scroll progress, not an independent timeline.

---

### 5.5 Soil Testing page — scroll triggers CSS classes

**Files:** `templates/soilTesting.html` (inline `<script>`), `static/css/soilTesting.css`.

**Markup pattern:**

```html
<div class="service-description" data-animate="slide-in-left">
```

**Flow:**

1. **`animateOnScroll()`** runs on **`scroll`** and **`load`**.
2. For each `[data-animate]` element, it reads **`getBoundingClientRect().top`** vs **`window.innerHeight`** to see if the block is **near** entering the viewport (threshold ~100px from bottom).
3. It compares **current scroll position** to **`lastScrollTop`** to guess scroll **direction**:
   - Scrolling **down** and element is in view → **`classList.add(element.dataset.animate)`** (e.g. add class `slide-in-left`).
   - Scrolling **up** and element is far below → **`classList.remove(...)`** to allow replay or reverse.
4. CSS classes like **`.slide-in-left`** apply **`animation: slideInLeft 1.2s ease forwards`**, which runs the **`@keyframes slideInLeft`** block (opacity 0→1, translateX -50px → 0).

**Rendering:** Adding the class triggers the browser’s **CSS animation** subsystem (not the same code path as Lottie). The animation runs on a **time** duration (1.2s), **once per add**, unlike the coin which is **purely scroll-scrubbed**.

---

### 5.6 Summary comparison (this project)

| Technique | Driven by | Render path | Used on |
|-----------|-----------|-------------|---------|
| DotLottie | **Time** (`autoplay`, `loop`) | Custom element + JSON decode + canvas/SVG draw per frame | `index.html` (hero + finance) |
| CSS `transition` | **State change** (hover, etc.) | Browser style interpolation | Nav, buttons, cards site-wide |
| CSS `@keyframes` + class | **Time** after class added | Browser CSS animation engine | Soil Testing slides |
| JS `transform` / `opacity` on scroll | **Scroll position** | Inline styles → compositor | Home coin (`script.js`) |

---

### 5.7 Script load order on the home page (end of `index.html`)

1. **`dotlottie-player.mjs`** (module) — registers and upgrades Lottie players.
2. **`script.js`** (classic script) — attaches scroll listener for the coin.

Lottie players are in the **body above** these scripts, so when the module runs, the DOM already contains `<dotlottie-player>` nodes to upgrade.

---

## 6. File map (frontend)

```
templates/          # Jinja HTML pages
static/
  css/              # Page-specific stylesheets
  js/               # script.js, signup.js
  images/           # Photos, icons (referenced from templates)
```

Each major screen typically has **one HTML file** and **one matching CSS file** (e.g. `loans.html` + `loans.css`).

---

## 7. Known HTML issue (home page)

In `index.html`, a stray `` ` `` character appears after the financial assistance section (before the horizontal card). That can break layout or validation; remove that character if you see odd rendering.

---

## 8. Summary

- **Frontend = Flask + Jinja templates + static CSS/JS.**
- **Rich motion = DotLottie (JSON animations from the web) + CSS transitions/keyframes + JS scroll logic** on the home and soil-testing pages.
- **No single animation framework** (no GSAP, no Framer Motion); it’s a mix of web components, native CSS, and small vanilla scripts.
- **Section 5** above walks through **how the browser renders** each type (DOM/CSSOM, layout vs composite, Lottie fetch + frame loop, scroll handlers vs CSS animation engine).

For questions about a specific page, open its template in `templates/` and its stylesheet in `static/css/` together.

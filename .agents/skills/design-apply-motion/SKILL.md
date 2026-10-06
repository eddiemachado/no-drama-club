---
name: apply-motion
description: Motion and interaction design expert for UI animations. Use when implementing transitions, animating UI elements, or deciding whether/how to animate. Covers decision-making, implementation recipes, performance, and accessibility.
version: '1.2'
triggers:
  - animate
  - animation
  - transition
  - motion
  - framer motion
  - hover effect
  - scroll animation
  - enter animation
  - exit animation
  - spring animation
  - fade in
  - fade out
  - slide in
  - slide out
  - prefers-reduced-motion
  - AnimatePresence
  - layoutId
  - keyframes
  - easing
  - interactive feedback
  - button press
  - toast notification
  - modal animation
  - drawer animation
  - stagger
  - FLIP
  - clip-path reveal
  - transform origin
  - will-change
  - GPU animation
  - interruptible
---

# Motion Design

You are a senior design engineer with a trained eye for motion that feels right — not just motion that runs. Your bias is toward **motion that earns its place**. Default to less motion, not more — every animation must justify itself before it gets written.

***

## Three Lenses

Use **Emil Kowalski's** lens to decide IF something should animate (restraint, speed — the Raycast standard). Use **Jakub Krehel's** techniques for HOW to animate in production (subtle polish). Use **Jhey Tompkins'** approach for creative CSS and portfolio contexts. State your weighting before implementing — don't apply Emil's 300ms rule to a kids app.

| Project Type                        | Primary | Secondary | Selective                     |
| ----------------------------------- | ------- | --------- | ----------------------------- |
| Productivity tool (Linear, Raycast) | Emil    | Jakub     | Jhey (onboarding only)        |
| SaaS dashboard                      | Emil    | Jakub     | Jhey (empty states)           |
| Kids app / Educational              | Jakub   | Jhey      | Emil (high-freq interactions) |
| Creative portfolio                  | Jakub   | Jhey      | Emil (high-freq interactions) |
| Marketing / landing page            | Jakub   | Jhey      | Emil (forms, nav)             |
| Mobile app                          | Jakub   | Emil      | Jhey (delighters)             |
| E-commerce                          | Jakub   | Emil      | Jhey (product showcase)       |

***

## 1. Decision Gate

### Should This Animate?

| Frequency                                      | Decision                     |
| ----------------------------------------------- | ---------------------------- |
| 100+/day (keyboard shortcuts, command palette) | No animation. Ever.          |
| Tens/day (hover effects, list navigation)      | Remove or drastically reduce |
| Occasional (modals, drawers, toasts)           | Standard animation           |
| Rare / first-time (onboarding, celebrations)   | Can add delight              |

**Never animate keyboard-initiated actions.** Raycast has no open/close animation. That is the optimal experience for something used hundreds of times a day.

### Valid Purposes

Every animation must answer: **"Why does this animate?"**

* **Spatial consistency** — toast enters and exits the same direction, making swipe-to-dismiss intuitive

* **State indication** — a morphing button shows the state changed

* **Feedback** — button scales down on press, confirming the interface heard the user

* **Explanation** — a marketing animation showing how a feature works

* **Preventing jarring changes** — elements appearing without transition feel broken

"It looks cool" on a frequently-seen element is not a valid purpose.

> "The best animation is that which goes unnoticed." If users consciously comment on an animation every time they see it, it's too prominent. Exception: kids apps where delight is the goal.

***

## 2. Implementation Hierarchy

When deciding whether and how to implement any animation, work through this order — prefer earlier answers over later ones:

1. **Delete** — is this high-frequency, keyboard-triggered, or purposeless? Don't animate it.
2. **Reduce** — can a shorter duration, smaller transform, or fewer animated properties do the job?
3. **Choose the right easing** — `ease-out` entering, `ease-in` exiting, custom curves always
4. **Set origin / physicality** — correct `transform-origin`; start at `scale(0.95)` not `scale(0)`
5. **Ensure interruptibility** — use transitions or springs, not keyframes, for triggered elements
6. **Stay on GPU** — animate `transform`/`opacity`; use WAAPI for programmatic CSS
7. **Apply asymmetric timing** — slow the deliberate phase, snap the system response
8. **Add polish** — blur to mask crossfades, stagger for groups, spring for "alive" feel
9. **Ship accessible** — add `prefers-reduced-motion` + hover gating; match product personality

***

## 3. Scoping: Where to Add Motion

Missing animations are often worse than poorly-tuned ones. Before implementing, search for **conditional renders without transitions** to find every place that needs motion:

```bash
# Conditional renders: {condition && <Component />}
grep -rn "&&\s*(" --include="*.tsx" --include="*.jsx" .

# Ternary UI swaps: {condition ? <A /> : <B />}
grep -rn "?\s*<" --include="*.tsx" --include="*.jsx" .
```

For each result: Is it wrapped in `<AnimatePresence>`? Does the component have enter/exit animations? No to both = **motion gap**.

Common gap locations: settings/inspector panels with mode switches, tab content, loading → content transitions, toast systems, error states, expandable sections.

***

## 4. Core Techniques

### Enter Animation Recipe (Jakub)

```jsx
initial={{ opacity: 0, translateY: 8, filter: "blur(4px)" }}
animate={{ opacity: 1, translateY: 0, filter: "blur(0px)" }}
transition={{ type: "spring", duration: 0.45, bounce: 0 }}
```

Blur creates a "materializing" effect — element comes into focus, not just fades in. For full container slides: `translateY: "calc(-100% - 4px)"`.

> **Performance note**: `translateY` here is a Framer shorthand prop (runs on main thread). Acceptable for one-shot mount animations. For animations that run while the page is loading or under sustained interaction, use `transform: "translateY(8px)"` instead. Also: `filter: blur()` is a paint operation — keep blur ≤ 8px, especially in Safari where heavy blur is expensive.

**Modern CSS entry** (`@starting-style` — no JS needed, Chrome 117+ / Safari 17.5+):

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 400ms ease-out, transform 400ms ease-out;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

### Exit Animation Subtlety (Jakub)

Exits must be subtler than enters — the user's focus is moving to what comes next.

```jsx
// Don't mirror the enter:
exit={{ translateY: "calc(-100% - 4px)" }}

// Use a subtle fixed value:
exit={{ translateY: "-12px", opacity: 0, filter: "blur(4px)" }}
```

Exception: user-initiated dismissal, error clearing, full-page directional transitions.

### Duration by Element Type (Emil)

| Element                  | Duration      |
| ------------------------ | ------------- |
| Button press feedback    | 100–160ms     |
| Tooltips, small popovers | 125–200ms     |
| Dropdowns, selects       | 150–250ms     |
| Modals, drawers          | 200–500ms     |
| Marketing / explanatory  | Can be longer |

**Rule**: UI stays under 300ms. A 180ms dropdown feels more responsive than a 400ms one even at the same load time.

### Easing (Emil + Jhey)

**Never use** **`ease-in`** **for UI animations.** It starts slow — exactly when users are watching most closely. **Always use custom Bézier curves.** Built-in CSS easings lack strength.

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);   /* UI interactions entering */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* On-screen movement, A→B */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like drawers/sheets */
```

| Easing        | Use For                                    |
| ------------- | ------------------------------------------ |
| `ease-out`    | Elements entering view                     |
| `ease-in`     | Elements leaving view (only)               |
| `ease-in-out` | State changes while on screen              |
| `spring`      | Interactive, gesture-driven, interruptible |
| `linear`      | Loops, spinners, marquees, progress        |

### Spring Animations (Emil + Jakub)

Springs simulate real physics and carry velocity when interrupted — CSS keyframes restart from zero.

```js
{ type: "spring", duration: 0.45, bounce: 0 }    // Professional, no overshoot
{ type: "spring", duration: 0.5, bounce: 0.2 }   // Slightly playful
{ type: "spring", stiffness: 300, damping: 30 }  // Traditional physics
```

`bounce: 0` = smooth deceleration. Reserve bounce > 0 for playful/kids contexts only.

**Use springs for**: drag interactions, gestures that can be interrupted mid-motion, elements that should feel "alive" (Dynamic Island-style).

### Interactive Feedback (Emil)

```css
/* Tactile press feedback */
button { transition: transform 160ms ease-out; }
button:active { transform: scale(0.97); }

/* Hover — always gate for touch devices */
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.02); }
}
```

**Never animate from** **`scale(0)`.** Nothing in the real world appears from nothing.

```jsx
// BAD
initial={{ scale: 0 }}

// GOOD
initial={{ scale: 0.95, opacity: 0 }}
animate={{ scale: 1, opacity: 1 }}
```

**Tooltip delay pattern** (Emil): first tooltip = delay + animation; subsequent tooltips in same group = instant.

```css
.tooltip[data-instant] { transition-duration: 0ms; }
```

**Velocity-based dismissal** (swipe/drag):

```js
const velocity = dragDistance / elapsedTime;
if (velocity > 0.11) dismiss(); // fast short flicks should work, not just long drags
```

### Asymmetric Timing (Emil)

Slow where the user is deciding; fast where the system responds.

```css
/* Press: slow and deliberate */
button:active .overlay { transition: clip-path 2s linear; }

/* Release: snappy */
.overlay { transition: clip-path 200ms ease-out; }
```

### Icon State Transitions (Jakub)

```jsx
<AnimatePresence mode="wait">
  {isCopied ? (
    <motion.div key="check"
      initial={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      exit={{ opacity: 0, scale: 0.8, filter: "blur(4px)" }}
    >
      <CheckIcon />
    </motion.div>
  ) : (
    <motion.div key="copy" ...><CopyIcon /></motion.div>
  )}
</AnimatePresence>
```

### Shared Layout / FLIP (Jakub)

```jsx
// Card in list view:
<motion.div layoutId="card-123" className="small-card" />

// Same card expanded:
<motion.div layoutId="card-123" className="large-card" />
```

Keep `layoutId` elements **outside** `AnimatePresence` — putting them inside causes initial/exit animations to conflict with the layout animation.

### Interruptibility (Emil)

**CSS keyframes cannot be redirected mid-flight.** Use transitions with state classes:

```css
.toast { transform: translateY(100%); transition: transform 400ms ease; }
.toast.mounted { transform: translateY(0); }
```

**WAAPI** — JavaScript control with CSS-level GPU performance:

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

**Decision**: CSS for predetermined animations; Framer/springs for dynamic/interruptible/gesture-driven; WAAPI when you need JS control with GPU-level performance.

### Origin-Aware Animations (Emil)

```css
/* Dropdown from button → expand from the button */
.dropdown { transform-origin: top center; }

/* Component library support */
.popover { transform-origin: var(--radix-popover-content-transform-origin); }
.popover { transform-origin: var(--transform-origin); } /* Base UI */
```

**Modals are exempt** — they stay `transform-origin: center` (not anchored to a trigger).

### Clip-Path Reveals (Emil)

Hardware-accelerated. No layout shifts. Smoother than `width`/`height`.

```css
.reveal {
  clip-path: inset(0 0 100% 0);
  animation: reveal 1s forwards cubic-bezier(0.77, 0, 0.175, 1);
}
@keyframes reveal { to { clip-path: inset(0 0 0 0); } }
```

Uses: scroll reveals, tab color transitions (duplicate + clip), hold-to-confirm fills, comparison sliders.

### Stagger (Emil + Jhey)

```css
.item { animation: fadeIn 300ms ease-out forwards; opacity: 0; }
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

**30–80ms between items.** Never block interaction while stagger plays.

### Advanced CSS (Jhey)

**`@property`** — type-declared custom properties that can be interpolated:

```css
@property --hue {
  syntax: '<number>';
  initial-value: 0;
  inherits: false;
}
@keyframes rainbow { to { --hue: 360; } }
```

**`linear()`** — pure CSS springs, bounce, elastic: linear-easing-generator.netlify.app

**`animation-fill-mode: backwards`** — prevents elements flashing at full opacity before their delayed animation starts.

### Blur as a Signal (Jakub)

Use `filter: blur()` to signal state: entering = blur → sharp; losing relevance = sharp → blur. Brief blur during crossfades masks imperfections when timing alone isn't enough. Keep blur ≤ 8px for animation — heavier blur is expensive, especially in Safari.

### Cohesion (Emil)

Motion must match the component's personality and the rest of the product. A playful component can be bouncier; a dashboard stays crisp and fast. When unsure whether motion feels right, the strongest move is often to delete it.

***

## 5. Performance

### Rendering Model

| Step          | Properties                                            | Cost             |
| ------------- | ----------------------------------------------------- | ---------------- |
| **Composite** | `transform`, `opacity`                                | Cheap — GPU only |
| **Paint**     | `color`, `border`, `filter`, `gradient`, `mask`       | Medium           |
| **Layout**    | `width`, `height`, `top`, `left`, `margin`, `padding` | Expensive        |

### Never Patterns

* Animate layout properties (`width`/`height`/`top`/`left`/`margin`/`padding`)

* Interleave layout reads and writes in the same frame

* Drive animation from scroll events — use Scroll/View Timelines or IntersectionObserver

* Run `requestAnimationFrame` loops without a stop condition

* Update a CSS variable on a **parent** to drive a child transform — triggers style recalc on all children; set `element.style.transform` directly instead

### Framer Motion: Shorthand vs. Full Transform (Emil)

Shorthand props are **not** GPU-accelerated:

```jsx
// NOT hardware-accelerated — drops frames when main thread is busy
<motion.div animate={{ x: 100 }} />

// GPU-accelerated — stays smooth under load
<motion.div animate={{ transform: "translateX(100px)" }} />
```

This matters when the browser is simultaneously loading content or running scripts. One-shot mount animations are low-risk; continuous / scroll-driven / drag animations must use full transform strings.

### `will-change`

```css
.animated-button { will-change: transform, opacity; } /* targeted — fine */
* { will-change: transform; }                          /* wasteful — avoid */
```

Budget: 0–3 elements = fine; 4–10 = test on low-end devices; 10+ = reconsider approach.

***

## 6. Accessibility (Mandatory — No Exceptions)

**Reduced motion means gentler, not zero.** Keep opacity and color transitions that aid comprehension. Remove movement and position-based animations.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```jsx
const shouldReduceMotion = useReducedMotion();
const closedX = shouldReduceMotion ? 0 : '-100%';
```

**Gate hover animations for touch devices** — touch fires hover on tap, causing false positives:

```css
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); }
}
```

Avoid vestibular triggers: large-scale zoom, spin, parallax. Looping ambient animations must be pauseable.

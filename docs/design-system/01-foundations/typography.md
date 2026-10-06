---
summary: >
  Type scale, font families/weights, line-height rules, approved
  heading+body pairings, and usage rules.
triggers: [font, type, typography, type scale, heading, weight, line-height]
related: [data-display.text]
---

# Typography

- Always use typography tokens [TODO: token location]
- Never use a hardcoded or custom value for `font-size`, `font-family`, `font-weight`, or `line-height`. Always use the tokens listed above.
- Do not override font size or styles within design system components [TODO: component library]
- `text-h1` appears at most once per screen; `text-h2`–`text-h4` may repeat within a page.
- Never render a heading (`h1`, `h2`, `h3`, `h4`) using `font-family-body`. Always use `font-family-heading`. 
- Never render a non heading using `font-family-heading` or `font-family-display`. Always use `font-family-body`.
- When displaying overlines, always use `text-overline`. Never use `text-caption` or style it manually.
- When displaying numbers in the UI, use `font-family-monospace` and `font-variant-numeric: tabular-nums`.
- Never style text with a font size smaller than `text-caption` (10px).
- Never pair `text-h4` and `text-body` in the same block (no visible hierarchy). Review the pairing rules below.

- Use `text-base` as the default style for all UI text.
- Use `text-small` for metadata, bylines, or when paired with other text to create heirarchy.
- Use `text-caption` for the [TODO: differentiate this and small]

Use the table below to understand which tokens to use for each. [TODO: we may not need this due to token setup]

TODO: add this to token data, not here

| Style | Class | font-size | line-height | font-family | font-weight |
|---|---|---|---|---|---|
| h1 | `text-h1` | `font-scale-h1` | `font-line-height-h1` | `font-family-heading` | `font-weight-strong` |
| h2 | `text-h2` | `font-scale-h2` | `font-line-height-h2` | `font-family-heading` | `font-weight-strong` |
| h3 | `text-h3` | `font-scale-h3` | `font-line-height-h3` | `font-family-heading` | `font-weight-strong` |
| h4 | `text-h4` | `font-scale-h4` | `font-line-height-h4` | `font-family-heading` | `font-weight-strong` |
| body | `text-body` | `font-scale-body` | `font-line-height-body` | `font-family-body` | `font-weight-regular` |
| small | `text-small` | `font-scale-small` | `font-line-height-small` | `font-family-body` | `font-weight-regular` |
| caption | `text-caption` | `font-scale-caption` | `font-line-height-caption` | `font-family-body` | `font-weight-regular` |


## Headings

- Never override or style a heading within a design system component [TODO: component library]
- Used for page, card, or section titles.
- Never using headings for more than 2 sentences of text
- Never truncate a heading. If it's too long, rewrite it to be shorter
- Never use status colors (guidelines at [.color.md](color.md)) on a heading

`h1` — page/screen title. At most one per screen.

`h2` — section headers

`h3` — card/module title, nested sections with a container that already contains an `h2`

`h4` — secondary sections, notifications


### Styling

If you need to style an element as another (e.g. `h3` as `h1`), you can use the styles as a class.

TODO: fix this section once we agree

```
<h3 class="styledas-h1">This is a headline</h3>
```

## Type pairings

Pairings are how to use two different styles together. Each pairing has a `gap` between the two elements.

- Only use a `gap` if you are pairing text elements in a group
- Only use `gap` tokens for gap spacing, never hard coded values (e.g. `8px`) or primitives (e.g. `spacing-1`)
- `gap` guidelines are found in `.spacing.md`

| Pairing | Gap token |
|---|---|
| `h1` + `body` | `gap-md` |
| `h2` + `body` | `gap-md` |
| `h3` + `body` | `gap-md` |
| `h4` + `small` | `gam-sm` |
| `small` + `caption` | `gap-sm` |
| `overline` + `h1` or `h2` | `gap-md` |
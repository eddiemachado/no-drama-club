---
summary: >
  TODO - radius description
triggers: [radius, corner-radius, border radius, rounded]
related: [foundations.elevation, foundations.spacing]
---

# Radius

Use [TODO: token location] for applying border-radius to an element. **Never** use hard coded values (e.g. `8px`) or primitive tokens (e.g. `radius-1`) for border-radius.

- Never override the border-radius within a design system component [TODO: component library]

## Nesting elements

When nesting containers or cards within a parent. Use `radii-container` on the parent container and `radii-nested` on the nested container. If the nested container is a `Card` component, do not override the border-radius, as the `radii-card` value is the same as `radii-nested`.
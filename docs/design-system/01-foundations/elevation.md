---
summary: >
  TODO - elevation description
triggers: [elevation, box-shadow, heirarchy, shadow]
related: [foundations.spacing]
---

# Elevation

Use [TODO: token location] for applying elevation to an element. **Never** use hard coded values (e.g. `8px`) or primitive tokens (e.g. `elevation-100`) for padding.

- Never override the box-shadow within a design system component [TODO: component library]
- Only use a `mask` when displaying Dialogs. Use the `effects-mask` token on the mask element.
- All elements within a container should have the same (or no) elevation.
- Do not apply elevation to elements within an element that is `elevation-floating` (e.g. Dialog, Modal, Toast, etc)
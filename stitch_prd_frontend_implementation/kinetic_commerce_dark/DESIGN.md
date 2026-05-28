---
name: Kinetic Commerce Dark
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c6c5d5'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#908f9e'
  outline-variant: '#454653'
  surface-tint: '#bdc2ff'
  primary: '#bdc2ff'
  on-primary: '#131e8c'
  primary-container: '#818cf8'
  on-primary-container: '#101b8a'
  inverse-primary: '#4953bc'
  secondary: '#44e2cd'
  on-secondary: '#003731'
  secondary-container: '#03c6b2'
  on-secondary-container: '#004d44'
  tertiary: '#f7bd3e'
  on-tertiary: '#402d00'
  tertiary-container: '#c08d00'
  on-tertiary-container: '#3e2b00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bdc2ff'
  on-primary-fixed: '#000767'
  on-primary-fixed-variant: '#2f3aa3'
  secondary-fixed: '#62fae3'
  secondary-fixed-dim: '#3cddc7'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005047'
  tertiary-fixed: '#ffdea3'
  tertiary-fixed-dim: '#f7bd3e'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5d4200'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  container-max: 1440px
---

## Brand & Style

This design system is a high-performance, dark-mode evolution of a modern commerce interface. It balances a **Corporate / Modern** foundation with subtle **Glassmorphism** accents to create a sense of depth and technical sophistication. The target audience includes professional merchants and data-driven consumers who require a focused, low-strain environment for high-frequency tasks.

The aesthetic is defined by deep, atmospheric surfaces and high-precision typography. It evokes a feeling of reliability, speed, and premium quality. Movement should be functional—snappy transitions and subtle glow effects—reinforcing the "Kinetic" nature of the brand while maintaining the calm and focus of a dark workspace.

## Colors

The palette is optimized for deep-space readability and visual hierarchy. 

- **Primary (Indigo):** Shifted to a lighter, more vibrant tint (#818CF8) to ensure AA contrast compliance against dark surfaces. It is used for primary actions, active states, and focus indicators.
- **Secondary (Teal):** A high-energy accent used for success states, growth metrics, and secondary callouts.
- **Surface:** The foundational layer uses a near-black Navy (#020617) to minimize eye strain.
- **Surface Container:** Elements like cards, sidebars, and modals use a lighter Navy-Gray (#1E293B) to create structural separation without relying on heavy borders.
- **Functional Colors:** Error states use a soft coral-red, and warnings use a muted amber to prevent "vibrating" against the dark background.

## Typography

Typography is built for clarity and data density. 

- **Headlines:** Hanken Grotesk provides a sharp, contemporary edge. Titles use high-contrast white-off-white (#F8FAFC) to pop against the dark canvas.
- **Body:** Inter is used for its exceptional legibility at small sizes. Text colors are tiered (Slate 200 to Slate 400) to establish information hierarchy.
- **Labels/Data:** JetBrains Mono is utilized for technical data, SKUs, and monochromatic labels to provide a distinct "utility" feel.

Always ensure a minimum contrast ratio of 4.5:1 for body text. Avoid pure white (#FFFFFF) for long-form text to prevent "halation" effects on high-brightness screens.

## Layout & Spacing

The design system utilizes a **Fluid Grid** model based on an 8px square baseline. 

- **Desktop:** 12-column grid with 24px gutters. Content is contained within a 1440px max-width wrapper.
- **Tablet:** 8-column grid with 20px gutters and 24px side margins.
- **Mobile:** 4-column grid with 16px gutters and 16px side margins.

Horizontal spacing is used to group related commerce items (e.g., product image and price), while generous vertical rhythm (32px - 64px) separates distinct sections like "Recommended" or "Cart Summary." Padding within surface containers should be consistent (typically 16px or 24px) to maintain the clean, structured look.

## Elevation & Depth

Depth is conveyed through **Tonal Layers** and **Glassmorphism**, rather than traditional heavy shadows.

1.  **Level 0 (Base):** The primary surface color (#020617).
2.  **Level 1 (Cards/Sections):** A slightly lighter fill (#1E293B) with a 1px low-opacity border (#334155) to define edges.
3.  **Level 2 (Modals/Popovers):** Surface-container color with a subtle `backdrop-filter: blur(12px)` and a very soft, diffused deep-blue shadow (0px 10px 30px rgba(0,0,0,0.5)).
4.  **Interactive States:** Hovering over a card should increase its border brightness or add a subtle primary-tinted glow rather than increasing shadow distance.

## Shapes

The shape language is **Rounded**, providing a sophisticated and approachable feel that softens the "coldness" often associated with dark, technical interfaces.

- **Buttons & Inputs:** 0.5rem (8px) corner radius.
- **Cards & Modals:** 1rem (16px) corner radius.
- **Status Chips:** Full pill-shape for high-contrast distinction from other UI elements.

Small UI details like checkboxes use the `rounded-sm` (4px) setting to maintain a precise, geometric appearance at small scales.

## Components

- **Buttons:** Primary buttons use a solid Indigo (#818CF8) fill with dark navy text for maximum legibility. Secondary buttons use a ghost style with a 1px Slate-700 border and Indigo text.
- **Input Fields:** Backgrounds should be slightly darker than their parent container with a subtle 1px border. On focus, the border transitions to Primary Indigo with a soft outer glow.
- **Cards:** Use the Level 1 Elevation (Slate-800). Content inside should have clear padding (24px) and use the JetBrains Mono label for categories.
- **Chips:** Used for "In Stock" or "Category" tags. Use low-saturation background tints (e.g., translucent Teal for success) to keep the UI from becoming too colorful and distracting.
- **Data Tables:** Use subtle horizontal dividers (#334155) and avoid vertical lines. Zebra-striping is discouraged; use hover states to highlight rows instead.
- **Navigation:** Sidebars should use the most "sunken" appearance (Base Surface) to allow the main content area (Surface Container) to feel elevated and focused.
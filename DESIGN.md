---
name: "RVAS AI Starter Kit"
description: "A customer-delivery web documentation system for choosing and proving the next useful AI decision."
colors:
  rvap-blue: "#1A77E3"
  rvap-blue-dim: "#0078D4"
  deep-navy: "#032254"
  hero-navy: "#0F3A7A"
  hero-accent: "#BFDBFE"
  paper: "#F5F8FE"
  surface: "#FFFFFF"
  surface-soft: "#FAFBFD"
  surface-muted: "#EEF1FA"
  line: "#E3E6ED"
  line-soft: "#DDE6F7"
  ink: "#111827"
  muted-ink: "#47494E"
  faint-ink: "#6B7280"
  teal-accent: "#14868A"
  purple-accent: "#504092"
  success: "#16A34A"
  warning: "#CA8A04"
  danger: "#DC2626"
typography:
  display:
    fontFamily: "Aptos Display, Outfit, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(2.2rem, 5vw + 0.5rem, 4.2rem)"
    fontWeight: 700
    lineHeight: 1.06
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Aptos Display, Outfit, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.6rem, 3vw + 0.4rem, 2.6rem)"
    fontWeight: 700
    lineHeight: 1.06
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Aptos Display, Outfit, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.1rem, 2vw + 0.3rem, 1.5rem)"
    fontWeight: 700
    lineHeight: 1.06
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Aptos, Inter, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "Cascadia Code, JetBrains Mono, Fira Code, ui-monospace, SF Mono, monospace"
    fontSize: "0.70rem"
    fontWeight: 500
    letterSpacing: "0.26em"
rounded:
  sm: "7px"
  md: "12px"
  lg: "18px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "24px"
  xl: "40px"
  section: "88px"
components:
  button-primary:
    backgroundColor: "{colors.rvap-blue}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: "11px 22px"
    typography: "{typography.body}"
  button-primary-hero:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.deep-navy}"
    rounded: "{rounded.sm}"
    padding: "11px 22px"
    typography: "{typography.body}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "11px 22px"
    typography: "{typography.body}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "24px"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.muted-ink}"
    rounded: "{rounded.sm}"
    padding: "5px 11px"
    typography: "{typography.label}"
---

# Design System: RVAS AI Starter Kit

## Overview

**Creative North Star: "The Guided Foundry Atlas"**

The system feels like a calm working atlas for customer AI decisions: clean RVAP paper surfaces, decisive Microsoft blue signals, and route-like components that help a facilitator move from idea to scenario to proof. It is not a generic product-marketing skin. It is a customer-delivery interface that makes the next decision visible and keeps implementation details subordinate to evidence.

The dominant visual language is light, crisp, and navigational, with a deep navy hero plane used as the opening orientation moment. Compass rings, dot grids, mono coordinate labels, numbered steps, and rail panels create the sense of a guided journey without making the site feel decorative or game-like.

**Key Characteristics:**

- RVAP clean light surfaces with Deep Navy signal moments.
- Scenario-first information architecture expressed through cards, rails, badges, and journey maps.
- Outfit/Aptos-style display typography paired with practical Inter/Aptos body copy and JetBrains/Cascadia mono labels.
- Subtle motion and elevation that make interaction states clear without distracting from customer evidence.
- Crisp, navigational, and facilitator-friendly components.

## Colors

The palette is **RVAP Clean Light with Deep Navy Signal**: white and blue-white surfaces carry most reading work, RVAP Blue identifies actions and route signals, and Deep Navy is reserved for hero orientation or high-emphasis framing.

### Primary

- **RVAP Blue**: The primary action and signal color. Use it for CTAs, active chips, focus rings, links, route accents, and the center of compass or journey motifs.
- **Deep Navy**: The strongest brand anchor. Use it for heading ink and hero gradients, not for dense content backgrounds outside intentional orientation sections.

### Secondary

- **Journey Teal**: A supporting scenario or module accent for alternate paths, proof states, and non-primary decision categories.
- **Workshop Purple**: A supporting scenario or module accent for advanced, orchestration, or distinct route families.
- **Hero Accent Blue**: A pale blue emphasis used on dark hero text and subtle hero highlights.

### Neutral

- **RVAP Paper**: The page canvas. Use it as the default background so the site remains readable and customer-facing.
- **Surface White**: Cards, panels, nav, and content containers.
- **Soft Surface**: Slightly raised or grouped content blocks.
- **Rule Line**: Borders, dividers, card outlines, and grid separation.
- **Ink**: Primary body and navigation text.
- **Muted Ink**: Supporting text, descriptions, and nav defaults.
- **Faint Ink**: Metadata, placeholders, and secondary labels.

### Named Rules

**The Blue Signal Rule.** RVAP Blue should identify decisions and next actions; do not scatter it as generic decoration.

**The Navy Gateway Rule.** Deep Navy belongs to high-orientation surfaces such as heroes, slide-like openers, and major route frames. Most content should remain on light surfaces.

## Typography

**Display Font:** Aptos Display with Outfit, Segoe UI, and system sans fallbacks.  
**Body Font:** Aptos with Inter, Segoe UI, and system sans fallbacks.  
**Label/Mono Font:** Cascadia Code or JetBrains Mono with Fira Code and system mono fallbacks.

**Character:** The pairing is modern Microsoft workshop typography: confident display headings, highly readable body copy, and small mono labels that behave like coordinates in a journey map.

### Hierarchy

- **Display** (700, responsive clamp, tight line-height): Hero headings and major page openers. Use sparingly and keep line breaks intentional.
- **Headline** (700, responsive clamp, tight line-height): Section titles and primary page divisions.
- **Title** (700, responsive clamp, tight line-height): Card titles, panel headings, and compact content group labels.
- **Body** (400, 16px, 1.65 line-height): Main explanatory text, guides, lesson prose, and customer-facing content.
- **Label** (mono, small, wide tracking, uppercase): Eyebrows, badges, stage labels, IDs, route metadata, and stats labels.

### Named Rules

**The Coordinate Label Rule.** Mono uppercase labels should orient the reader, not shout at them. Keep them short, tracked, and paired with meaningful content.

## Layout

The layout is a responsive atlas grid. The shared container maxes out at 1200px with 24px mobile gutters and 40px desktop gutters. Major sections use generous vertical rhythm, with full sections around 88px and tighter content sections around 56px.

Home and route pages use a two-column hero at desktop widths, collapsing to a single column on smaller screens. Scenario and lesson pages use a content-plus-sidebar layout: the main narrative carries the journey while the sidebar exposes proof, decisions, and facilitator actions. Cards use auto-fit grids with minimum widths around 320-360px so the system can accept new scenarios without bespoke layout work.

**The Journey Before Catalog Rule.** Layout should first clarify the customer path, then expose the supporting reference library. Do not let dense implementation catalogs compete with scenario decision surfaces.

## Elevation & Depth

Depth is a hybrid of tonal layering, thin borders, and restrained shadows. Cards and panels are mostly flat at rest, separated by white surfaces, soft blue-gray fills, and rule lines. Shadows appear as ambient confidence on cards, hero glass stats, and hover states, never as heavy material stacks.

### Shadow Vocabulary

- **Page Glow** (`radial-gradient(900px 600px at 80% -10%, rgba(26, 119, 227, 0.10), transparent 65%)`): Background atmosphere behind the page.
- **Card Shadow** (`0 1px 3px rgba(3, 34, 84, 0.08), 0 4px 12px rgba(3, 34, 84, 0.06)`): Default card depth and hover lift.
- **Ambient Shadow** (`0 4px 20px -8px rgba(3, 34, 84, 0.12), 0 1px 3px rgba(3, 34, 84, 0.06)`): Higher-level surfaces and shared shell depth.
- **Hero Glass Shadow** (`0 24px 60px rgba(3, 34, 84, 0.28)`): Used only for translucent statistic blocks on dark hero surfaces.

### Named Rules

**The Flat-Until-Useful Rule.** Surfaces stay quiet until interaction or hierarchy needs lift. Use border, fill, and route color before adding more shadow.

## Shapes

Shapes are gently curved and practical. Small controls use 7px radii, cards and panels use 12-18px radii, and badges use tight 4-5px rounding. Borders are crisp and light; colored strips or 3px leading rules provide directionality for cards and decision panels.

Compass geometry and dotted grids are allowed as orientation motifs, especially in heroes or decision sections. They should stay atmospheric and low-opacity rather than becoming foreground decoration.

## Components

### Buttons

- **Shape:** Gently squared control radius (7px).
- **Primary:** RVAP Blue background with white text, 11px x 22px padding, 600 body weight, and subtle blue glow. In dark heroes, invert primary buttons to white with Deep Navy text.
- **Hover / Focus:** Hover reduces opacity or lightly shifts background; focus uses a 2px RVAP Blue outline with 2-3px offset.
- **Ghost:** Transparent surface with a rule-line border. On dark heroes, ghost buttons use white text and a translucent white border.

### Chips

- **Style:** Mono, compact, and filter-like. Default chips are transparent with Rule Line borders and Muted Ink text.
- **State:** Active chips fill with RVAP Blue or route accent color and switch to high-contrast text.

### Cards / Containers

- **Corner Style:** Large rounded cards (18px) for scenario and module cards; medium rounded panels (12px) for rails and steps.
- **Background:** Surface White or Soft Surface over RVAP Paper.
- **Shadow Strategy:** Border-first at rest, subtle lift on hover.
- **Border:** Rule Line borders define card edges; route cards may add a top gradient strip or left accent rule.
- **Internal Padding:** 22-24px for normal cards, 18-20px for compact cards.

### Inputs / Fields

- **Style:** Search and form fields sit on soft tinted surfaces with Rule Line borders and 7px corners.
- **Focus:** Border shifts to RVAP Blue; do not add heavy glows.
- **Disabled / Empty:** Use Faint Ink for placeholder and empty states.

### Navigation

Navigation is a sticky white glass bar with the RVAP full logo, compact text links, and a mobile hamburger. Links use Muted Ink by default, Ink on active or hover, and a soft muted background on selection. The GitHub link is treated as a utility link and should not compete with primary scenario navigation.

### Hero Compass

The hero compass is the signature visual device. It combines low-opacity rings, quadrant path strokes, center signal dots, and slow rotation that respects `prefers-reduced-motion`. Use it to imply orientation and progress, not literal technical architecture.

### Scenario Rails

Scenario and lesson sidebars use stacked panels with uppercase heads, concise body text, ordered journey lists, and action rails. They should read like facilitator notes: scannable, grounded, and easy to act from.

## Do's and Don'ts

### Do:

- **Do** preserve the RVAP light canvas and Deep Navy hero contrast.
- **Do** use mono labels for orientation metadata such as maturity, duration, stage, and route IDs.
- **Do** use cards, rails, and steps to show where the customer is in the decision journey.
- **Do** keep primary actions visibly blue or hero-inverted; secondary actions should stay quiet.
- **Do** respect reduced-motion settings for compass rotation and reveal animation.

### Don't:

- **Don't** turn the system into a dark terminal UI; dark navy is a gateway moment, not the default reading surface.
- **Don't** use RVAP Blue as background ornament everywhere. It must remain a decision/action signal.
- **Don't** add decorative diagrams, customers, proof, or claims that are not present in the product evidence.
- **Don't** replace the RVAP logo or Foundry icon vocabulary with unrelated icon styles.
- **Don't** make reference-library mechanics visually outrank the scenario playbooks.

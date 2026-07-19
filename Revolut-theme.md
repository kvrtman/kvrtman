# Revolut Theme

**Design analysis of the QuantumLight "Scale-up Playbooks"** (quantumlightcapital.com — the VC firm founded by Revolut's founder; the playbooks codify how Revolut was built and scaled).
This document describes the UI/design, business-data visualization, overall visualization, font, color, overall presentation and information structure of each section of the **Hiring Top Talent** and **Performance Management** playbooks, so the theme can be reproduced.

Analyzed 2026-07-19 from the live server-rendered pages (Next.js + Chakra UI/Emotion, diagram assets served from Contentful).

---

## 1. The Shared Design System (applies to every page)

### 1.1 UI / Design language

- **Flat, typographic, "fintech-minimal"** — the same visual DNA as Revolut's brand: near-black + white surfaces, one saturated electric blue accent, generous whitespace, rounded-corner geometry, zero photography inside content (the only photo on the site is the email-form illustration `form-image.jpg`).
- **Full-bleed horizontal bands** alternate between white content and black (`#000` / `#111111`) chrome: black top navigation bar, black hero/marketing bands, white article body, black footer.
- **Corner-radius scale** used everywhere: `7px` (small controls/pills), `10px` (badges, cards), `15px` (diagram panels/accordion frames), `20px` (large feature cards such as the blue "at a glance" card).
- **Vertical rhythm**: large sections separated by `2.75rem` (mobile) → `3.75rem` (desktop) margins; in-card padding up to `52px` top/bottom.
- Built with **Chakra UI** components (`chakra-text`, `chakra-stack`, `chakra-accordion`) styled through Emotion, so all styling ships inline with the HTML; one small global stylesheet defines the custom list/accordion behaviors.
- Subtle interaction states only: accordion hover = `blackAlpha.50` wash, focus = Chakra outline shadow, `0.4` opacity for disabled.

### 1.2 Font

| Role | Family | Size (mobile → desktop) | Weight | Notes |
|---|---|---|---|---|
| Page title (H1) | Basier Circle | 32px → **48px** | 700 | `line-height` ~111% |
| Section heading (H2) | Basier Circle | 24px → **34px** | 500 | often preceded by a 16px blue line icon |
| Sub-heading (H3) | Basier Circle | 21–25px | 500–700 | hub category cards use 16px → 25px, weight 500 |
| Body paragraph | Basier Circle | **16px** | 400 | `line-height: 24px`; list body 14px |
| Small/labels | Basier Circle | 14px | 400 | pagination labels, card descriptions |
| Captions/meta | Basier Circle | 12px → 16px | 400 | e.g. "4 minutes to read" badge, color `#969696` |
| Mono (rare) | SFMono/Menlo stack | — | — | Chakra default, effectively unused |

- **Typeface: "Basier Circle"** (atipo foundry) — a geometric circular grotesque, self-hosted as OTF. Three files are loaded with a deliberate **weight-shift trick**: `300 → BasierCircle-Regular.otf`, `400 → BasierCircle-Medium.otf`, `500 → BasierCircle-SemiBold.otf`. So "regular" text (400) actually renders Medium — this is what gives the site its slightly heavy, confident text color.
- Fallback stack (Chakra tokens): `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`.
- No letter-spacing manipulation, no uppercase transforms — hierarchy comes purely from size, weight and color.

### 1.3 Color

| Token | Hex | Usage |
|---|---|---|
| **Primary blue** | `#2D64E3` | The single accent: "at a glance" card fill + border, icons/strokes, links, buttons, diagram accents (secondary tone `rgba(39,104,227,1)` ≈ `#2768E3` for hovers/gradients) |
| Black | `#000000`, `#111111` | Nav bar, hero bands, footer, headings on white |
| White | `#FFFFFF` | Page background, text on dark bands |
| Panel gray | `#F4F4F4`, `#F5F5F5` | Diagram frames, quote/example panels, neutral cards |
| Border gray | `#E6E6E6` | Hairlines, dividers |
| Text grays | `#778089` (body secondary), `#6F7987`, `#969696` (meta/labels), `#636363`, `#B2B2B2` (footnotes), `#A5B0BB` (footer links) |
| White-alpha ladder (on dark) | `rgba(255,255,255, .18 / .3 / .48 / .64 / .8 / .92)` | Numbered-circle chips, secondary text, dividers on black/blue surfaces |
| Black-alpha | `rgba(0,0,0, .04–.1)` | Shadows, hover washes |

- **Rule of thumb**: one hue only. Everything is black/white/gray + `#2D64E3`. Even "success/error" palette entries (Chakra defaults) go unused in the playbooks.
- On dark surfaces, text de-emphasis is done with **white alpha steps**, not gray hex values.

### 1.4 Business data visualization (system-wide approach)

- **Every chart, table, scorecard, org chart and process diagram is a pre-rendered flat SVG** hosted on Contentful (`images.ctfassets.net`). There is no charting library, no HTML `<table>` for data, no interactivity — figures are designed like print artwork so typography (Basier Circle), the blue accent and stroke weights stay perfectly on-brand.
- Recurring figure types across the playbooks:
  - **Skills scorecards** (criteria rows × rating columns, rounded cells)
  - **Talent-bar / distribution charts** (bell-curve-like bars with a blue cutoff)
  - **Org charts** (simple → scaled recruitment/performance team trees)
  - **Funnels & process timelines** (numbered steps, left-to-right flows)
  - **Calculation walk-throughs** (performance-score & bonus-multiplier math, styled as SVG "tables": `Table_7.svg`, `Table_9.svg`, `Quotas.svg`)
  - **Comparison matrices** (equity vs cash, compensation matrix per level)
- Diagram canvases sit on white or `#F4F4F4` rounded panels (`15px`), thin gray strokes, blue highlights for the "important" series/cell.
- Large **stat typography** is used as data-viz on marketing bands (e.g. "10+ billion", "700,000" rendered as display-size headings).

### 1.5 Component inventory

| Component | Styling facts |
|---|---|
| **"This section at a glance" card** | The signature element opening every chapter: background `#2D64E3`, radius `20px`, 2px blue border with **no left border**, white text, `52px` vertical padding, custom bullet dots (8px white circles; nested bullets at 50% opacity), bold spans kept at weight 400 for tone-on-tone emphasis |
| Read-time badge | Gray pill, radius `10px`, text 12px → 16px `#969696`, "N minutes to read" |
| Accordion (`ql-accordion`) | Chakra accordion; hover `blackAlpha.50`; panels contain paragraphs + SVG figures; used for examples & step details |
| Dot list (`listDots`) | Custom bullets: 8px white dot (dark theme) positioned outside text |
| Numbered list (`listOrdered`) | CSS-counter chips: 32px circle, `rgba(255,255,255,.18)` fill, white bold number — used for the chapter index on dark hub bands |
| Chapter cards (hubs) | Category H3 (16→25px, weight 500) + 14–16px gray description + numbered chapter links `01…07` in white on dark |
| Prev / Next pagination | Bottom of every chapter: circular arrow icon + `Previous:`/`Next:` label, `#969696`, 14px → 16px |
| Email capture | "Don't miss out on new playbooks!" panel with `form-image.jpg` illustration and a form |
| Sidebar TOC | `sidebar-md` (desktop) / `sidebar-mobile` — chapter navigation beside the article column |

### 1.6 Information structure (both playbooks)

```
Playbook hub (e.g. /playbooks/hiring)
├── Hero band (black) — playbook title & intro
├── 3 phase groups (H3 category cards)
│      Hiring:      Identify top talent → Recruit at scale → Build the team
│      Performance: Set Foundations → Build Processes → Act on Results
├── Numbered chapter index 01–07 (white-on-dark, counter circles)
├── Email capture ("Don't miss out on new playbooks!")
└── Footer (black)

Chapter page (all 13 content pages share this template)
├── Sidebar TOC + "N minutes to read" badge
├── H1 (32→48px, 700)
├── ★ "This section at a glance" — blue summary card with dot bullets
├── 3–16 H2 sections (24→34px, 500), each mixing:
│      body text · SVG diagram(s) · accordions for examples/steps
└── Prev / Next chapter pagination
```

---

## 2. Section-by-Section Profiles

### 2.1 Hiring Top Talent — hub
`https://quantumlightcapital.com/playbooks/hiring` · 1 minute to read

- **UI/Design:** Landing/index layout, not an article: black hero band, three category cards, numbered chapter list on dark, email-capture panel. 24 `playbook-section` blocks; card radii 10px, pills 7px.
- **Business data visualization:** None (no diagrams); the "data" is the numbered chapter index itself. 7 small inline SVGs are icons/arrows only.
- **Overall visualization:** Dark-dominant marketing look; white and blue text on black; the only image is the form illustration.
- **Font:** Category H3s 16→25px weight 500; card descriptions 14→16px; chapter links 0.875rem white; hub uses more small sizes (10–12px legal/footer) than chapters.
- **Color:** Black bands with white/white-alpha text, `#2D64E3` CTAs, `rgba(255,255,255,.18)` number chips, gray `#F4F4F4/#F5F5F5` light panels.
- **Overall presentation:** A table of contents disguised as a landing page — sells the playbook then routes you into chapter 01.
- **Information structure:** 3 phase groups → *Identify top talent* (ch. 01–03), *Recruit at scale* (ch. 04–05), *Build the team* (ch. 06 + a "07 SPOTLIGHT | Revolut People" chapter) → numbered links `01 Scale-up Ready Profiles … 07`; closes with the email form ("Don't miss out on new playbooks!").

### 2.2 Scale-up Ready Profiles
`…/hiring/scale-up-ready-profiles` · 4 minutes to read

- **UI/Design:** Standard chapter template (read-time badge → H1 → blue at-a-glance card → article sections); 7 accordion buttons for expandable detail; gray `#F4F4F4` diagram panels (radius 15px).
- **Business data visualization:** 3 Contentful SVGs — "Scale-up ready profiles" trait diagram, a public variant, and "Why traditional hiring assumptions fail" (assumption-vs-reality comparison graphic).
- **Overall visualization:** Text-led with one figure per major claim; blue card up top acts as the visual anchor.
- **Font:** H1 48px/700 "Scale-up Ready Profiles"; H2 34px/500; body 16px/400 lh24; small print 12–14px.
- **Color:** White body, `#2D64E3` at-a-glance card + accents, `#F4F4F4` figure panels, black nav/footer bands.
- **Overall presentation:** Thesis-driven essay ("potential over experience") — each H2 argues one point, backed by a diagram; ends routing to the next chapter.
- **Information structure:** H1 → *This section at a glance* → *Potential over experience* → *Why traditional hiring assumptions fail* → *Three traits of a scale-up ready hire* → Prev: Hiring Top Talent / Next: Three Interviews for Success.

### 2.3 Three Interviews for Success
`…/hiring/three-interviews-for-success` · 2 minutes to read

- **UI/Design:** Chapter template; repeating pattern of H2 (interview type) + H3 "How the interview works"; no accordions on this page.
- **Business data visualization:** 4 SVGs — problem-solving **scorecard** (criteria × ratings grid), problem-solving interview graphics (PNG+SVG pair), and a **bar-raiser** flow diagram.
- **Overall visualization:** The scorecard SVGs are the star — table-like artwork with rounded cells and blue rating highlights.
- **Font:** Same scale; H3 sub-headers (21–25px/500-700) appear under each H2 to structure the walkthroughs.
- **Color:** System palette; `#E6E6E6` hairlines separating the three interview blocks.
- **Overall presentation:** A three-part recipe; each interview = concept intro then "How the interview works" procedural detail.
- **Information structure:** H1 → at a glance → *The problem-solving assessment* (+How it works) → *The bar-raiser* (+How it works) → *The people management & hiring assessment* (+How it works) → prev/next.

### 2.4 Setting a Talent Framework
`…/hiring/setting-a-talent-framework` · 4 minutes to read

- **UI/Design:** Chapter template + 7 accordions (role-definition examples).
- **Business data visualization:** 5 SVGs — "Setting a Talent Framework" steps 1–3, the **Talent bar** distribution chart (where to set the hiring bar), and a **Data-Analysis skill scorecard** example.
- **Overall visualization:** Sequential framework figures (1→2→3) give the page a step-by-step visual storyline; scorecard SVG doubles as a template readers copy.
- **Font / Color:** System scale & palette; blue used to mark the "bar" cutoff inside the talent-bar figure.
- **Overall presentation:** How-to guide culminating in a concrete example ("Example – Data Scientist") — concept → method → artifact.
- **Information structure:** H1 → at a glance → *How to build a talent framework* → *Defining roles* → *The talent bar* → *Example – Data Scientist* → prev/next.

### 2.5 Standardised Hiring Process
`…/hiring/standardised-hiring-process` · 8 minutes to read

- **UI/Design:** The longest, most component-dense chapter: **35 accordions** carrying step-by-step detail, objection-handling scripts and reference-call questions; numbered H3s (`1.`–`7.`) inside H2 umbrellas.
- **Business data visualization:** 8 SVGs — hiring-process document mockups, funnel/sourcing diagrams ("Standardizing Hiring 6/7"), problem-solving scorecard, "Managing common objections" graphic, and a checklist figure.
- **Overall visualization:** Heavy progressive disclosure — the page would be overwhelming flat, so accordions collapse the 7-step process into scannable stages.
- **Font / Color:** System scale; step numbers as part of H3 text (no special chips inside articles); blue accents in every figure.
- **Overall presentation:** An operations manual: numbered pipeline (kick-off doc → sourcing → screening → interviews → engaging → references → probation) with monitoring wrapped around it.
- **Information structure:** H1 → at a glance → *Standardising each step of hiring* → H3 steps 1–7 interleaved with H2 deep-dives (*A hiring process document in detail*, *A note on remote, high-density talent pools*, *Interviewer certification program*, *Managing common objections*, *Example reference call questions*) → *Monitoring the process* → prev/next.

### 2.6 Recruitment Team
`…/hiring/recruitment-team` · 5 minutes to read

- **UI/Design:** Chapter template + 14 accordions (role cards, examples).
- **Business data visualization:** 8 SVGs — the richest "org & metrics" set: simple vs **scaled recruitment org charts**, internal-recruitment-team diagram, RT role cards, **Hiring Volume** chart, **Performance-score calculation** walkthrough and **Quotas** table.
- **Overall visualization:** Organizational storytelling — trees for structure, tables/calculations for quotas and incentives, all as consistent SVG artwork.
- **Font / Color:** System scale & palette.
- **Overall presentation:** Business case → build → scale → measure: argues for in-house recruiting, then gives structures, roles, quotas and incentive math, ending in a worked example.
- **Information structure:** H1 → at a glance → *The case for an internal recruitment team* → *Building a recruitment powerhouse* → *Structuring and scaling the recruitment org* → *Recruitment team roles* → *Recruiter Quotas & Incentives* → *Example* → prev/next.

### 2.7 Playbook Example — (Data) Engineers
`…/hiring/playbook-example-engineers` · 6 minutes to read

- **UI/Design:** Simplest chapter — **no at-a-glance card, no accordions**; a flat reference document.
- **Business data visualization:** 4 SVGs — Data-Engineer role one-pager, **Skill-mastery** and **Specialised-skill scorecards**, and an end-to-end **Hiring process** flow.
- **Overall visualization:** Essentially a printed template pack rendered inline; figures dominate over prose.
- **Font / Color:** System scale; fewer size variants used (no 25px hub-style headings).
- **Overall presentation:** "Here is everything from the previous chapters applied to one role" — an artifact library: role definition → scorecards & talent bar → sourcing guidelines → process.
- **Information structure:** H1 *Playbook Example Data Engineers* → *About the role* → *Skills Scorecards & Talent Bar* → *Sourcing guidelines* → *Hiring process* → prev/next.

### 2.8 Performance Management — hub
`https://quantumlightcapital.com/playbooks/performance-management` · 1 minute to read

- **UI/Design:** Identical hub layout to 2.1 (26 `playbook-section` blocks, 9 inline icon SVGs).
- **Business data visualization:** None — numbered chapter index as the only "data".
- **Overall visualization / Font / Color:** Same dark marketing bands, category cards, numbered white-on-dark chapter list, blue CTAs, email capture.
- **Overall presentation:** Playbook cover + TOC; routes into 7 chapters.
- **Information structure:** 3 phase groups → *Set Foundations* → *Build Processes* → *Act on Results*; chapters `01 Talent Philosophy … 07 Compensation & Review Process`; email form; footer.

### 2.9 Talent Philosophy
`…/performance-management/talent-philosophy` · 3 minutes to read

- **UI/Design:** Chapter template, no accordions — a manifesto-style read.
- **Business data visualization:** 4 SVGs — "essence of high-performance culture" concept diagrams (tp-2/3/4 series).
- **Overall visualization:** Concept illustrations rather than data; blue at-a-glance card carries the summary.
- **Font / Color:** System scale & palette.
- **Overall presentation:** Principles chapter: defines the philosophy ("pay top of market, expect top performance") before the machinery in later chapters.
- **Information structure:** H1 → at a glance → *The essence of high-performance* → *Making it happen* → prev/next.

### 2.10 Performance Team
`…/performance-management/performance-team` · 2 minutes to read

- **UI/Design:** Chapter template, no accordions; short.
- **Business data visualization:** 4 SVGs — performance-team **org charts** (Group 301/302), **team-size scaling chart** (`2PT_team_size.svg`), team-profile diagram.
- **Overall visualization:** Mirrors the Recruitment Team chapter: trees + a sizing curve.
- **Font / Color:** System scale & palette.
- **Overall presentation:** Business case → responsibilities → structure → profiles; the org-design companion to the philosophy chapter.
- **Information structure:** H1 → at a glance → *The case for a performance team* → *Responsibilities* → *Team structure* → *Team profiles* → prev/next.

### 2.11 The Framework
`…/performance-management/the-framework` · 5 minutes to read

- **UI/Design:** Biggest accordion usage in the playbooks (**51 accordion buttons**) — every "Example – …" H2 expands into role-specific scorecards; 16 H2 sections.
- **Business data visualization:** 12 SVGs — the scorecard engine room: Deliverables examples (**Speed, Quality, Complexity**), Skills examples (**Data Scientist, Account Manager, Product Owner, Software Engineer**), Culture example (**"Get it done"**), plus framing diagrams (`Frame_48`, "Direct CEO mandate").
- **Overall visualization:** A pattern library of near-identical scorecard SVGs — repetition itself communicates "standardisation".
- **Font / Color:** System scale; slight extra use of 18px and 10–12px inside dense figures; one translucent panel `rgba(144,144,144,0.19)`.
- **Overall presentation:** The conceptual core: performance = Deliverables + Skills + Culture, each defined then instantiated per role via collapsible examples, ending with how scorecards run in practice.
- **Information structure:** H1 → at a glance → *What defines performance* → *Deliverables* (+3 example H2s) → *Skills* (+4 example H2s) → *Culture* (+1 example H2) → *Standardising performance via scorecards* → *Putting the scorecards into practice* → prev/next.

### 2.12 The Process
`…/performance-management/the-process` · 3 minutes to read

- **UI/Design:** Chapter template + 7 accordions.
- **Business data visualization:** 4 SVGs — **talent-bar** chart (performance edition), process flow (Group 21/23), and an **example score calculation** walkthrough.
- **Overall visualization:** One diagram per stage; calculation SVG shows the weighted math in brand style.
- **Font / Color:** System scale; translucent gray panel reused from 2.11.
- **Overall presentation:** Operational chapter: how reviews actually run against the bar, closing with worked scoring math.
- **Information structure:** H1 → at a glance → *The talent bar* → *Running the process* → *Example score calculation* → prev/next.

### 2.13 Career Trajectories
`…/performance-management/career-trajectories` · 6 minutes to read

- **UI/Design:** Chapter template + 20 accordions (level definitions, PIP steps).
- **Business data visualization:** 6 SVGs — **promotion-process** and **promotion-principles** diagrams, seniority-level chart (Group 16 / Frame 48), **underperformance** flow and **Performance Improvement Plan** timeline.
- **Overall visualization:** Career ladders and process flows; upward/downward paths both diagrammed.
- **Font / Color:** System scale & palette.
- **Overall presentation:** Covers both directions performance can send you — promotion machinery and improvement plans — each with an "Example" walkthrough.
- **Information structure:** H1 → at a glance → *Impact of performance on career progression* → *Path to promotion* → *Seniority levels* → *Example – Engineer* → *The promotion process* → *Improvement plan* → *Example – how a PIP is implemented* → prev/next.

### 2.14 Performance Bonuses
`…/performance-management/performance-bonuses` · 5 minutes to read

- **UI/Design:** Chapter template + 7 accordions; extra `#F4F4F4` panels (4) for the worked-example tables.
- **Business data visualization:** 8 SVGs — the most numeric chapter: bonus concept charts (bonuses-1/2/3/5/9), **bonus-multiplier tables** (`Table_7`, `Table_9`), and **equity-vs-cash** comparison (`6PB_equity_vs_cash.svg`).
- **Overall visualization:** SVG "spreadsheets" — multiplier grids with blue highlights on the exponential top-performer cells.
- **Font / Color:** System scale; more 12–14px usage (dense tables).
- **Overall presentation:** Argument ("reward top talent exponentially") → mechanism (multiplier) → end-to-end example → process → instrument choice (cash vs equity).
- **Information structure:** H1 → at a glance → *Using bonuses to reward top talent exponentially* → *The bonus multiplier* → *An end-to-end example* → *Bonus award process* → *Cash vs Equity bonuses* → prev/next.

### 2.15 Compensation & Review Process
`…/performance-management/compensation-review-process` · 3 minutes to read

- **UI/Design:** Chapter template + 26 accordions (scenario walk-throughs).
- **Business data visualization:** 3 SVGs — **pay-review flow** (`7CRP_pay_review_1.svg`) and **compensation matrix** diagrams (compensation-1/2), e.g. the level × performance pay matrix for an Engineer.
- **Overall visualization:** Matrix-centric; three "Example" H2s reuse the same matrix with different highlighted paths (promoted employee / A-player / general review).
- **Font / Color:** System scale & palette.
- **Overall presentation:** Final chapter closes the loop: pay philosophy → matrix → review process → three worked scenarios; ends the playbook's prev/next chain.
- **Information structure:** H1 → at a glance → *Paying the right price for talent* → *Example – Matrix for an Engineer* → *Pay review process* → *Example – Promoted Employee* → *Example – A-player* → *Example – General Review* → prev.

---

## 3. Rebuild Cheat-Sheet (design tokens)

```css
:root {
  /* color */
  --ql-blue: #2D64E3;            /* single accent */
  --ql-blue-alt: #2768E3;
  --ql-black: #000000;           /* bands: nav, hero, footer */
  --ql-black-soft: #111111;
  --ql-white: #FFFFFF;
  --ql-panel: #F4F4F4;           /* diagram/example panels */
  --ql-panel-alt: #F5F5F5;
  --ql-border: #E6E6E6;
  --ql-text-secondary: #778089;
  --ql-text-meta: #969696;
  --ql-text-footnote: #B2B2B2;
  --ql-chip-on-dark: rgba(255,255,255,.18);

  /* radius */
  --ql-radius-sm: 7px;   /* pills, small controls */
  --ql-radius-md: 10px;  /* badges, cards */
  --ql-radius-lg: 15px;  /* diagram frames, accordions */
  --ql-radius-xl: 20px;  /* feature cards ("at a glance") */

  /* type — Basier Circle, weight-shifted */
  /* @font-face: 300→Regular.otf, 400→Medium.otf, 500→SemiBold.otf */
  --ql-h1: 700 48px/1.11 'Basier Circle';   /* 32px mobile */
  --ql-h2: 500 34px/1.2  'Basier Circle';   /* 24px mobile */
  --ql-h3: 500 25px/1.2  'Basier Circle';   /* 16px mobile */
  --ql-body: 400 16px/24px 'Basier Circle';
  --ql-small: 400 14px/21px 'Basier Circle';
  --ql-meta: 400 12px/1rem 'Basier Circle'; /* 16px desktop */

  /* spacing rhythm */
  --ql-section-gap: 3.75rem;   /* 2.75rem mobile */
  --ql-card-pad-y: 52px;
}
```

**Signature moves to copy:** (1) one blue on black/white/gray, nothing else; (2) open every document with a blue radius-20 "at a glance" summary card with dot bullets; (3) render all business data as brand-styled flat SVG scorecards/tables/flows instead of live charts; (4) number the chapters `01…07` in translucent white circles on dark; (5) read-time badge + prev/next pagination to make long operational content feel like a book.

# POS Product Team — H2 2026 Performance System

Owner: Kurt Molina. Aligned to the 29 Jun KPI call with Ivan Grytsenko and the
QuantumLight (Revolut) performance-management playbook.

## The system in one paragraph

The north star is **absolute PBT in pesos, per product line** (QRPh, Online,
Moto/Deals, Credit Line, Solar, Offline). PBT = Volume (disbursements) ×
Profitability %. Below that sit the Tier 2 diagnostic questions (margin too
thin? cost of risk eating margin? opex undiluted for lack of scale?) and the
Tier 3 input metrics the team moves daily. A phase overlay (Star / Question
mark → push volume; Cash cow → maintain, no PM) decides which lever each line
pushes. Delivery management is a separate axis: **Deliverables = (Speed +
Quality) × Complexity, judged by business impact, not activity.**

## Each owner carries three KPIs

| Owner | Lines | D1 line outcome | D2 key driver |
|---|---|---|---|
| JV Manlangit | Moto & SAP | Moto ~P15M/mo (Nhat-gated) | Disb per active agent P315K → 500K+ |
| Anton Betia | Deals & Solar | Deals P25→50→100M/mo staged at +NPM | Acceptance & conversion (reject salvage) |
| Manzil Balani | Deals BD | Managed-account disb (ProTech, Maxicare, 3Cat) | Merchants live; ticket uplift P1,000–2,000 |
| Elias Marcella | Credit Line & Card | CL utilization & drawdown (target ~15 Aug) | Card break-even on interchange @ CAC P300–500 |
| Jastin Lagumbay | QRPh & Onboarding | QRPh ~P107M/mo run rate | Onboarding cycle time; zero config errors |

D3 for every owner: agreed roadmap steps delivered on pace (Delivery
Scoreboard). Enablers: Nhat (PBT-per-line model), Jenny (metric-tree
dashboard), Billy (release quality gate).

## Targets are set bottom-up (Ivan's method)

Where we are → why (margin / risk / opex diagnosis) → agreed actions →
estimated impact per action → deadline ⇒ the target. No numbers out of
nowhere; a miss traces to a delivery gap that is visible per project in the
tracker.

## Cadence

- **Weekly (Mon standup):** Executive Project Tracker v2 — status, due vs
  delivered, blockers, impact. ClickUp stays the source of truth (linked per row).
- **Monthly:** KPI readout, target vs actual per line (KPI Targets H2 tab),
  fed by Nhat's PBT model and Jenny's dashboard.
- **Quarterly (first: end Sep):** QuantumLight Product Owner scorecard per PM —
  Culture, Skills, Deliverables = (Speed + Quality) × Complexity vs the
  seniority talent bar → A-player / Above bar / Underperformer; A-players
  calibrated to 15–25%.
- **Semi-annual:** promotions on sustained A-player grades; pay to benchmark;
  bonus multiplier = scorecard grade × KPI attainment.

## Files

- `POS_Product_H2_2026_KPI_OnePager.pptx` — the one-pager for the Ivan call.
- `Executive_Project_Tracker_v2.xlsx` — the weekly tracker, now with Impact /
  Due / Delivered columns, a formula-driven Delivery Scoreboard, and the KPI
  Targets H2 tab. Yellow cells = to fill (first pass due at the 21 Jul standup).
- The QuantumLight Performance Review Template (Product Owner) is used as-is
  for quarterly reviews — set each PM's seniority on the scorecard, paste
  their 3 KPIs into its KPI space, keep one copy per person per quarter.
- `src/` — the generators for both files, for regeneration.

## To agree with Ivan

1. Tier 0 = PBT per line; phase classification per line.
2. Volume targets: QRPh 107, Moto 15, Deals ramp timing (25→50→100), CL
   utilization target date 15 Aug.
3. Adopt the PO scorecard + talent bar for the 5 PMs; first review end of Sep.
4. Bonus linkage: scorecard grade × KPI attainment, team and lead.

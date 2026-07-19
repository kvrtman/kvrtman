# POS Product Team, H2 2026 Performance System

Owner: Kurt Molina. Proposed framework for discussion and approval with Ivan
Grytsenko, combining the 29 Jun KPI alignment call with the QuantumLight
(Revolut) performance-management playbook. All number KPIs are placeholders
until set bottom-up and approved.

## The system in one paragraph

The north star is absolute PBT in pesos, per product line (QRPh, Online,
Moto/Deals, Credit Line, Solar, Offline). PBT = Volume (disbursements) x
Profitability %. Below that sit the Tier 2 diagnostic questions (margin too
thin? cost of risk eating margin? opex undiluted for lack of scale?) and the
Tier 3 input metrics the team moves daily. A phase overlay (Star and Question
mark lines push volume; Cash cow lines are maintained with no PM) decides
which lever each line pushes. Delivery management is a separate axis:
Deliverables = (Speed + Quality) x Complexity, judged by business impact, not
activity.

## Each owner carries three KPIs (targets TBD, set bottom-up)

| Owner | Lines | D1 line outcome | D2 key driver |
|---|---|---|---|
| JV Manlangit | Moto and SAP | Moto monthly disbursement (target TBD, Nhat-gated) | Disbursement per active sales agent (uplift TBD) |
| Anton Betia | Deals and Solar | Deals monthly disbursement, staged ramp at positive NPM (stages TBD) | Acceptance and conversion (salvage plan on rejects) |
| Manzil Balani | Deals BD | Managed-account disbursement (ProTech, Maxicare, 3Cat) | New merchants live, ticket uplift (TBD) |
| Elias Marcella | Credit Line and Card | CL utilization and drawdown (target set ~30 days post-launch) | Per-card break-even on interchange (CAC target TBD) |
| Jastin Lagumbay | QRPh and Onboarding | QRPh monthly run rate (target TBD) | Onboarding cycle time, zero config errors |

D3 for every owner: agreed roadmap steps delivered on pace. Enablers: Nhat
(PBT per line model), Jenny (metric tree dashboard), Billy (release quality
gate).

## Targets are set bottom-up (Ivan's method)

Where we are, then why (margin, risk or opex diagnosis), then agreed actions,
then estimated impact per action, then a deadline. That estimate becomes the
target. No numbers out of nowhere; a miss traces to a delivery gap that is
visible per project in the tracker.

## Access model

- The Executive Project Tracker is shared with the whole team. Policy: everyone
  sees what everyone else is doing; one centralized tracker.
- The Delivery Scoreboard is a separate file kept by Kurt only. Individual
  delivery scores are never visible between team members.

## Cadence

- Weekly (Monday standup): tracker walk, status, due vs delivered, blockers,
  impact. ClickUp stays the source of truth (linked per row).
- Monthly: KPI readout, target vs actual per line (KPI Targets H2 tab), fed by
  Nhat's PBT model and Jenny's dashboard.
- Quarterly (first at end of Sep): QuantumLight Product Owner scorecard per PM.
  Culture, Skills, Deliverables = (Speed + Quality) x Complexity against the
  seniority talent bar. Grades: A-player, Above bar, Underperformer, with
  A-players calibrated to 15-25%.
- Semi-annual: promotions on sustained A-player grades, pay to benchmark,
  bonus multiplier = scorecard grade x KPI attainment.

## Files

- `POS_Product_H2_2026_KPI_OnePager.pptx`: the one-pager for the Ivan call.
- `Executive_Project_Tracker_v2.xlsx`: the shared weekly tracker with Impact,
  Due and Delivered columns and the KPI Targets H2 tab. Yellow cells are
  placeholders to fill (first pass at the 21 Jul standup).
- `Delivery_Scoreboard.xlsx`: Kurt-only. Per-owner delivery stats computed from
  a Delivery Log tab that mirrors the tracker's Master Rollup; refresh by paste
  or IMPORTRANGE in Google Sheets.
- The QuantumLight Performance Review Template (Product Owner) is used as-is
  for quarterly reviews: set each PM's seniority, answer the yes/no statements,
  paste their 3 KPIs into its KPI space, one copy per person per quarter.
- `src/`: the generators for all three files.

## To agree with Ivan

1. Tier 0 = PBT per line, phase classification per line.
2. Set the placeholder targets bottom-up: QRPh and Moto run rates, Deals ramp
   sizes and timing, CL utilization target date.
3. Adopt the PO scorecard and talent bar for the 5 PMs, first review end of Sep.
4. Bonus linkage: scorecard grade x KPI attainment, team and lead.

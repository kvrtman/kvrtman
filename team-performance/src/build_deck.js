// POS Product H2 2026 KPI one-pager, single 16:9 slide for the Ivan call.
// Framework for discussion and approval: all number KPIs shown as placeholders.
// BillEase brand: white-dominant, structural blue 203AA9, ink text, rationed color.
const pptxgen = require("pptxgenjs");

const BLUE = "203AA9", INK = "1A1A1A", GRAY = "8A8A82";
const BLUE_T = "ECEEF8";                       // light blue tint
const GREEN = "1E8E5A", GREEN_T = "E7F4EE";    // margin
const RED = "C0392B", RED_T = "FBEAE7";        // risk
const AMBER = "9C6B1D", AMBER_T = "FCF3E0";    // opex
const BAND = "F6F4EF";
const F = "Arial";

const p = new pptxgen();
p.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
const slide = p.addSlide();
slide.background = { color: "FFFFFF" };

// ---------- header ----------
slide.addText([
  { text: "POS Product Team KPIs, H2 2026", options: { fontSize: 23, bold: true, color: BLUE } },
], { x: 0.45, y: 0.28, w: 9.2, h: 0.42, fontFace: F, margin: 0, align: "left" });
slide.addText("Kurt Molina, for alignment with Ivan, Jul 2026", {
  x: 9.7, y: 0.33, w: 3.18, h: 0.3, fontFace: F, fontSize: 9, color: GRAY, align: "right", margin: 0,
});
slide.addText(
  "Proposed framework for discussion and approval. North star: absolute PBT per line, three tiers, phase aware, delivery managed on business impact. Combines our 29 Jun call with the QuantumLight (Revolut) playbook. All number KPIs are placeholders until set bottom-up.",
  { x: 0.45, y: 0.70, w: 12.43, h: 0.28, fontFace: F, fontSize: 9.5, color: INK, margin: 0 }
);

const secLabel = (x, y, w, text) =>
  slide.addText(text, { x, y, w, h: 0.24, fontFace: F, fontSize: 10.5, bold: true, color: BLUE, margin: 0, charSpacing: 1 });

// ---------- column 1: metric tree ----------
const c1x = 0.45, c1w = 4.02;
let y = 1.06;
secLabel(c1x, y, c1w, "1. THE METRIC TREE"); y += 0.32;

// Tier 0
slide.addText([
  { text: "TIER 0 NORTH STAR: absolute PBT (pesos) per line", options: { fontSize: 9.5, bold: true, color: "FFFFFF", breakLine: true } },
  { text: "QRPh, Online, Moto/Deals, Credit Line, Solar, Offline", options: { fontSize: 8.5, color: "DDE3F7" } },
], { shape: p.ShapeType.roundRect, rectRadius: 0.05, fill: { color: BLUE }, x: c1x, y, w: c1w, h: 0.56, fontFace: F, margin: 0.06, align: "center", valign: "middle" });
y += 0.64;

slide.addText("PBT  =  Volume (disbursements)  x  Profitability %", {
  x: c1x, y, w: c1w, h: 0.22, fontFace: F, fontSize: 9.5, bold: true, color: INK, align: "center", margin: 0,
});
y += 0.28;

// Tier 1
const chip = (x, y, w, h, fill, color, lines) =>
  slide.addText(lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } })), {
    shape: p.ShapeType.roundRect, rectRadius: 0.04, fill: { color: fill },
    x, y, w, h, fontFace: F, fontSize: 8.5, bold: true, color, align: "center", valign: "middle", margin: 0.03,
  });
chip(c1x, y, 1.96, 0.42, BLUE_T, BLUE, ["TIER 1: VOLUME", "portfolio size and share"]);
chip(c1x + 2.06, y, 1.96, 0.42, BLUE_T, BLUE, ["TIER 1: PROFITABILITY", "margin %"]);
y += 0.5;

// Tier 2 diagnostic
chip(c1x, y, 1.28, 0.44, GREEN_T, GREEN, ["MARGIN", "pricing too thin?"]);
chip(c1x + 1.37, y, 1.28, 0.44, RED_T, RED, ["RISK", "CoR eating margin?"]);
chip(c1x + 2.74, y, 1.28, 0.44, AMBER_T, AMBER, ["OPEX", "undiluted, no scale?"]);
y += 0.54;

// Tier 3 inputs
slide.addText([
  { text: "TIER 3: what the team moves daily", options: { bold: true, fontSize: 8.5, color: INK, breakLine: true } },
  { text: "Margin: markup rate, take-up rate, MDR", options: { breakLine: true, color: GREEN } },
  { text: "Risk: cost of risk, NPM per merchant", options: { breakLine: true, color: RED } },
  { text: "Opex: opex per disbursement, sales-agent economics", options: { breakLine: true, color: AMBER } },
  { text: "Volume: disb run rate, acceptance and conversion, active partners, CL utilization", options: { color: BLUE } },
], { x: c1x, y, w: c1w, h: 1.06, fontFace: F, fontSize: 8.5, color: INK, margin: 0, lineSpacingMultiple: 1.12 });
y += 1.14;

slide.addText([
  { text: "Phase overlay decides the lever:  ", options: { bold: true } },
  { text: "Star and Question marks push volume (all PMs sit here). Cash cow (Offline) is maintain only, no PM. Low profitability is acceptable today where the phase says grow the size." },
], { shape: p.ShapeType.roundRect, rectRadius: 0.04, fill: { color: BAND }, x: c1x, y, w: c1w, h: 0.78, fontFace: F, fontSize: 8.5, color: INK, margin: 0.07, valign: "middle" });
y += 0.92;

slide.addText("NUMBERS POLICY", {
  x: c1x, y, w: c1w, h: 0.2, fontFace: F, fontSize: 8.5, bold: true, color: INK, margin: 0, charSpacing: 0.5,
});
y += 0.22;
slide.addText(
  "Every number KPI is a placeholder (P__) until we set it bottom-up and approve it together. First pass on this call, then a standing review at the monthly KPI readout.",
  { x: c1x, y, w: c1w, h: 0.7, fontFace: F, fontSize: 8.5, color: "3D3D3D", margin: 0, lineSpacingMultiple: 1.14, valign: "top" }
);

// ---------- column 2: owner KPIs + target method ----------
const c2x = 4.72, c2w = 4.42;
y = 1.06;
secLabel(c2x, y, c2w, "2. OWNER KPIs, THREE EACH"); y += 0.24;
slide.addText("D1 line outcome, D2 key driver, D3 delivery (all owners)", {
  x: c2x, y, w: c2w, h: 0.2, fontFace: F, fontSize: 8.5, italic: true, color: GRAY, margin: 0,
});
y += 0.26;

const owners = [
  ["JV Manlangit, Moto and SAP", "Moto monthly disbursement P__M (Nhat-gated), disbursement per active sales agent P__"],
  ["Anton Betia, Deals and Solar", "Deals monthly disbursement P__M staged at positive NPM, acceptance and conversion (salvage plan on rejects)"],
  ["Manzil Balani, Deals BD", "Managed-account disbursement (ProTech, Maxicare, 3Cat), new merchants live, ticket uplift P__"],
  ["Elias Marcella, Credit Line and Card", "CL utilization and drawdown (target set ~30d post-launch), per-card break-even at CAC P__"],
  ["Jastin Lagumbay, QRPh and Onboarding", "QRPh monthly run rate P__M, onboarding cycle time from signed to live, zero config errors"],
];
owners.forEach(([name, kpis], i) => {
  slide.addText([
    { text: name, options: { bold: true, color: INK, breakLine: true } },
    { text: kpis, options: { color: "3D3D3D" } },
  ], {
    x: c2x, y, w: c2w, h: 0.485, fontFace: F, fontSize: 8.5, margin: 0.045,
    fill: i % 2 === 0 ? { color: BAND } : undefined, valign: "middle", lineSpacingMultiple: 1.05,
  });
  y += 0.525;
});
slide.addText([
  { text: "D3, every owner: ", options: { bold: true } },
  { text: "agreed roadmap steps delivered on pace, scored weekly.   ", options: {} },
  { text: "Enablers: ", options: { bold: true } },
  { text: "Nhat (PBT per line model), Jenny (metric tree dashboard), Billy (release quality gate).", options: {} },
], { x: c2x, y, w: c2w, h: 0.44, fontFace: F, fontSize: 8.5, color: INK, margin: 0, lineSpacingMultiple: 1.08 });
y += 0.56;

secLabel(c2x, y, c2w, "3. TARGETS ARE SET BOTTOM-UP"); y += 0.28;
slide.addText([
  { text: "Where we are → why (margin, risk or opex?) → agreed actions → estimated impact → deadline → the target.", options: { bold: true, breakLine: true } },
  { text: "e.g. a reject-salvage plan on Deals: estimate how much can be converted, put a date on it, and that estimate becomes the month's target.", options: { italic: true, color: "3D3D3D", breakLine: true } },
  { text: "No targets out of nowhere. A miss traces to a delivery gap, visible per project in the tracker.", options: {} },
], { x: c2x, y, w: c2w, h: 1.15, fontFace: F, fontSize: 8.8, color: INK, margin: 0, lineSpacingMultiple: 1.14, paraSpaceAfter: 4 });

// ---------- column 3: cadence + asks ----------
const c3x = 9.42, c3w = 3.46;
y = 1.06;
secLabel(c3x, y, c3w, "4. TRACKING RHYTHM, STRICT FROM JULY"); y += 0.3;
const cadence = [
  ["Weekly: Monday standup", "Exec tracker, shared with the whole team: status, due vs delivered, blockers, impact. Detail stays in ClickUp (linked per row). Delivery scores are kept separately by Kurt."],
  ["Monthly: KPI readout", "Target vs actual per line, from Nhat's PBT model and Jenny's dashboard."],
  ["Quarterly: scorecard (first at end of Sep)", "Revolut-style review per PM: Culture, Skills, and Deliverables = (Speed + Quality) x Complexity, against the seniority talent bar. Grades: A-player, Above bar, Underperformer. A-players calibrated to 15-25%."],
  ["Semi-annual: promotion and pay", "Promotions on sustained A-player grades, pay to benchmark, bonus multiplier = grade x KPI attainment."],
];
cadence.forEach(([h, b]) => {
  const bodyLines = Math.ceil(b.length / 52);
  const hgt = 0.21 + bodyLines * 0.155;
  slide.addText([
    { text: h, options: { bold: true, color: BLUE, breakLine: true } },
    { text: b, options: { color: INK } },
  ], { x: c3x, y, w: c3w, h: hgt, fontFace: F, fontSize: 8.5, margin: 0, lineSpacingMultiple: 1.08 });
  y += hgt + 0.115;
});

y += 0.06;
slide.addText([
  { text: "5. TO AGREE TODAY", options: { bold: true, fontSize: 10.5, color: BLUE, charSpacing: 1, breakLine: true } },
  { text: "1.  Tier 0 = PBT per line, phase per line as shown", options: { breakLine: true } },
  { text: "2.  Set the placeholder targets bottom-up: QRPh and Moto run rates, Deals ramp sizes and timing, CL utilization date", options: { breakLine: true } },
  { text: "3.  Adopt the PO scorecard and talent bar for the 5 PMs, first review end of Sep", options: { breakLine: true } },
  { text: "4.  Bonus linkage: scorecard grade x KPI attainment, team and lead", options: {} },
], {
  shape: p.ShapeType.roundRect, rectRadius: 0.05, fill: { color: BLUE_T },
  x: c3x, y, w: c3w, h: 2.16, fontFace: F, fontSize: 8.8, color: INK, margin: 0.1,
  valign: "top", lineSpacingMultiple: 1.1, paraSpaceAfter: 3,
});

// ---------- footer ----------
slide.addText(
  "Working docs: Executive Project Tracker v2 (weekly, shared, linked to the KPI tree and ClickUp), KPI Targets H2 tab (monthly), QuantumLight Product Owner scorecard (quarterly), Delivery Scoreboard (Kurt only).",
  { x: 0.45, y: 7.14, w: 12.43, h: 0.22, fontFace: F, fontSize: 8, color: GRAY, margin: 0 }
);

p.writeFile({ fileName: "POS_Product_H2_2026_KPI_OnePager.pptx" }).then(() => console.log("deck written"));

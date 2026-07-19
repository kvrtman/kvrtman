#!/usr/bin/env python3
"""Build Executive_Project_Tracker_v2.xlsx from the original tracker.

Shared with the whole team. Keeps the original structure and BillEase brand
(white-dominant, blue 203AA9 headers, ink text, rationed color) and adds what
Ivan's approach requires: Impact, Due and Delivered columns plus a KPI Targets
H2 tab. All number KPIs are placeholders until agreed. Delivery scores live in
a separate private Delivery Scoreboard file kept by Kurt.
"""
import datetime as dt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

SRC = 'tracker.xlsx'
OUT = 'Executive_Project_Tracker_v2.xlsx'

BLUE = '203AA9'
INK = '1A1A1A'
GRAY = '8A8A82'
BAND = 'F6F4EF'
FILLME = 'FFF3C9'   # yellow = cell for the owner to fill

STATUS_STYLE = {  # value -> (font_rgb, bold, fill_rgb)
    'Blocked':     ('C0392B', True, 'FBEAE7'),
    'Cancelled':   ('8A8A82', True, 'ECE8E1'),
    'Completed':   ('1E8E5A', True, 'E7F4EE'),
    'In Progress': ('203AA9', True, 'ECEEF8'),
    'Not Started': ('8A8A82', True, 'F2EEE7'),
}

F_TITLE = Font(name='Arial', size=13, bold=True, color=BLUE)
F_HDR   = Font(name='Arial', size=10, bold=True, color='FFFFFF')
F_BODY  = Font(name='Arial', size=10, color=INK)
F_BODYB = Font(name='Arial', size=10, bold=True, color=INK)
F_NOTE  = Font(name='Arial', size=9,  color=GRAY)
F_BLUEB = Font(name='Arial', size=10, bold=True, color=BLUE)
FILL_HDR  = PatternFill('solid', fgColor=BLUE)
FILL_BAND = PatternFill('solid', fgColor=BAND)
FILL_FILL = PatternFill('solid', fgColor=FILLME)
THIN_BOT = Border(bottom=Side(style='thin', color='D9D9D9'))
WRAP = Alignment(wrap_text=True, vertical='top')
TOP = Alignment(vertical='top')

OWNER_TABS = {'JV': 'JV Manlangit', 'Anton': 'Anton Betia', 'Manzil': 'Manzil Balani',
              'Elias': 'Elias Marcella', 'Jastin': 'Jastin Lagumbay'}

# --- seeded values: facts already stated in the team's own docs; no KPI numbers ---
IMPACTS = {
    ('JV', 'Motorcycle Loans (KServico)'): 'Moto monthly run rate, gated by Nhat',
    ('Anton', 'Special Deals Offer to Low-Risk Customers'): 'Conversion lift on low-risk base, size with Nhat before comms',
    ('Manzil', 'Deals Merchant BD Pipeline'): 'New merchants live and disbursing, ticket uplift',
    ('Elias', 'Credit Line (Launch)'): 'CL utilization and drawdown, target set ~30 days post-launch',
    ('Elias', 'Access Card'): 'Per-card break-even on interchange at target CAC',
    ('Jastin', 'QRPh Chargeback Escalation (Netbank/AUB)'): 'Protects the QRPh run rate',
    ('Jastin', 'Integrate Merchant Guide to Billease Docs'): 'Fewer onboarding tickets via self-serve guide',
}
DUES = {('Anton', 'Special Deals Offer to Low-Risk Customers'): dt.date(2026, 7, 20)}
DELIVERED = {
    ('JV', 'SAP Announcement & Quiz Module v1'): dt.date(2026, 7, 3),
    ('JV', 'Credit Line - Agent Announcement (SAP)'): dt.date(2026, 7, 16),
    ('Manzil', 'Maxicare PRIMA Launch on Deals'): dt.date(2026, 7, 10),
}

# KPI Key Drivers cells rewritten so no number KPI is pre-committed
KD_OVERRIDES = {
    'A2': 'Each owner carries 3 metrics: line outcome, key driver, delivery. Number targets are placeholders (TBD) until agreed with Ivan; they live on KPI Targets H2.',
    'C5': 'Deals monthly disbursement at positive NPM (staged ramp, stage targets TBD)',
    'D6': 'New merchants live and disbursing. Ticket uplift target TBD',
    'C7': 'Moto (KServico) monthly disbursement (run-rate target TBD, gated by Nhat)',
    'D7': 'Disbursement per active sales agent (uplift target TBD)',
    'D8': 'Card unit economics: per-card break-even on interchange (CAC target TBD)',
    'C9': 'QRPh monthly disbursement run rate (target TBD, star line)',
}

src = openpyxl.load_workbook(SRC)
wb = openpyxl.Workbook()
wb.remove(wb.active)

def title(ws, cell, text):
    ws[cell] = text; ws[cell].font = F_TITLE

def note(ws, cell, text):
    ws[cell] = text; ws[cell].font = F_NOTE

def hdr_row(ws, row, headers, start_col=1):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(vertical='center')
    ws.row_dimensions[row].height = 21.75

def style_status(cell):
    s = STATUS_STYLE.get(cell.value)
    if s:
        cell.font = Font(name='Arial', size=10, bold=s[1], color=s[0])
        cell.fill = PatternFill('solid', fgColor=s[2])

def set_widths(ws, widths):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w

# ---------------------------------------------------------------- README
ws = wb.create_sheet('README')
set_widths(ws, {'A': 2.5, 'B': 112})
L = [
    ('T', 'Executive Project Tracker v2, POS Product Team (H2 2026)'),
    ('B', 'One file, shared with the whole team. One tab per owner plus a consolidated Master. Linked to the PBT Metric Tree KPIs discussed with Ivan.'),
    ('S', ''),
    ('H', 'Purpose'),
    ('B', 'One row per project, straight to the point. ClickUp stays the main working document and source of truth.'),
    ('B', 'This sheet is the executive-level view: what the project is, whether it is moving, what it is expected to move (Impact), and whether we delivered when we said we would.'),
    ('B', 'Everyone sees everything here. The point is a single, centralized view of what the team is doing.'),
    ('S', ''),
    ('H', 'What is new in v2 (after the 29 Jun KPI alignment with Ivan)'),
    ('B', 'Impact (bottom-up): every project carries the estimated business impact and its assumption. Targets come from agreed actions, never out of nowhere.'),
    ('B', 'Due and Delivered: the date agreed with the owner, and the date it actually shipped. Delivery is managed by business result, not by number of emails sent.'),
    ('B', 'KPI Targets H2 tab: per-line targets, target vs actual by month. All number targets are placeholders for now; yellow cells are set bottom-up and agreed with Ivan, then filled monthly.'),
    ('B', 'Delivery track record: Due and Delivered feed a separate Delivery Scoreboard file kept by Kurt. The shared work is visible to all; individual delivery scores stay private.'),
    ('S', ''),
    ('H', 'The tabs'),
    ('B', 'Master Rollup: every project across all owners, ranked. Keep this Viewer-only for the team.'),
    ('B', 'KPI Targets H2: line-level targets (Tier 0 and Tier 1), reviewed monthly.'),
    ('B', 'One tab per owner (JV, Anton, Manzil, Elias, Jastin). Each person maintains only their own tab.'),
    ('B', 'KPI Key Drivers: the PBT Metric Tree metrics that the KPI column points to (3 per owner: D1 line outcome, D2 key driver, D3 delivery).'),
    ('S', ''),
    ('H', 'The columns'),
    ('B', 'Project, Status, Priority, KPI Key Driver, Impact (bottom-up), Due, Delivered, Summary, ClickUp or BRD Link. The Master also has an Owner column.'),
    ('B', 'Status and Priority are dropdowns. Pick from the list so the ranking stays consistent.'),
    ('B', 'Yellow cells are blanks the owner must fill: Impact and Due before a project enters In Progress; Delivered when it ships (backfill for completed items).'),
    ('S', ''),
    ('H', 'Status and Priority values'),
    ('B', 'Status: Not Started, In Progress, Blocked, Completed, Cancelled.'),
    ('B', 'Priority: Urgent, High, Normal, Low.'),
    ('S', ''),
    ('H', 'Ranking rule'),
    ('B', 'Rows are ordered Urgent, High, Normal, Low, with Completed and Cancelled sent to the bottom.'),
    ('B', 'To re-sort after edits, select the table, then use Data, then Sort range, by Priority.'),
    ('S', ''),
    ('H', 'Operating cadence'),
    ('B', 'Weekly standup: walk the Master top-down, blocked and overdue first, and update Due and Delivered. Details live in ClickUp via the link column.'),
    ('B', 'Monthly: KPI readout on the KPI Targets H2 tab against Nhat\'s PBT-per-line model and Jenny\'s metric-tree dashboard.'),
    ('B', 'Quarterly: individual reviews on the QuantumLight (Revolut) Product Owner scorecard. Culture, Skills, and Deliverables = (Speed + Quality) x Complexity. The Impact column and the private Delivery Scoreboard are the evidence for business impact and Speed. A-players calibrated to 15-25% of the team.'),
    ('S', ''),
    ('H', 'Lock each tab to one person (done inside Google Sheets)'),
    ('B', '1. Share the whole file with the 5 owners as Editor, and the wider team as Viewer.'),
    ('B', '2. On each owner tab, use Data, then Protect sheets and ranges, then Set permissions, then Custom.'),
    ('B', '3. Add only that owner\'s email plus your own, then Done.'),
    ('S', ''),
    ('H', 'Design'),
    ('B', 'Minimalist, per the Billease brand: white-dominant, structural blue 203AA9 headers, ink text, rationed color.'),
]
r = 2
for kind, text in L:
    if kind == 'S':
        r += 1; continue
    cell = ws.cell(row=r, column=2, value=text)
    cell.font = F_TITLE if kind == 'T' else (F_BLUEB if kind == 'H' else F_BODY)
    r += 1

# ------------------------------------------------- owner tabs + master data
def enrich(tab, rows):
    for d in rows:
        key = (tab, d['project'])
        d['impact'] = IMPACTS.get(key, '')
        d['due'] = DUES.get(key, '')
        d['delivered'] = DELIVERED.get(key, '')
    return rows

owner_rows = {}
for tab in OWNER_TABS:
    s = src[tab]
    rows = []
    for row in s.iter_rows(min_row=4):
        if row[0].value is None:
            continue
        rows.append(dict(project=row[0].value, status=row[1].value, prio=row[2].value,
                         kpi=row[3].value, summary=row[4].value,
                         link=row[5].value if len(row) > 5 else None))
    owner_rows[tab] = enrich(tab, rows)

HDRS = ['Project', 'Status', 'Priority', 'KPI Key Driver', 'Impact (bottom-up)',
        'Due', 'Delivered', 'Summary', 'ClickUp / BRD Link']
OWNER_WIDTHS = {'A': 32, 'B': 13, 'C': 11, 'D': 26, 'E': 34, 'F': 9, 'G': 9.5, 'H': 50, 'I': 46}

def write_project_row(ws, r, vals, status_col, banded):
    status = vals[status_col - 1]
    for i, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=i, value=v if v != '' else None)
        c.font = F_BODY; c.border = THIN_BOT
        c.alignment = TOP
        if banded:
            c.fill = FILL_BAND
    ws.cell(row=r, column=1).font = F_BODYB
    style_status(ws.cell(row=r, column=status_col))
    return status

def yellow_blanks(ws, r, status, cols):
    for col, kind in cols.items():
        c = ws[f'{col}{r}']
        if c.value is None:
            if (kind == 'open' and status not in ('Completed', 'Cancelled')) or \
               (kind == 'done' and status == 'Completed'):
                c.fill = FILL_FILL

for tab, full in OWNER_TABS.items():
    ws = wb.create_sheet(tab)
    set_widths(ws, OWNER_WIDTHS)
    ws.freeze_panes = 'A4'
    ws['A1'] = f'{tab}: edit only this tab. Yellow = fill me (Impact and Due before In Progress; Delivered when shipped).'
    ws['A1'].font = F_NOTE
    hdr_row(ws, 3, HDRS)
    r = 4
    for i, d in enumerate(owner_rows[tab]):
        vals = [d['project'], d['status'], d['prio'], d['kpi'], d['impact'],
                d['due'], d['delivered'], d['summary'], d['link']]
        write_project_row(ws, r, vals, status_col=2, banded=(i % 2 == 1))
        for col in ('F', 'G'):
            ws[f'{col}{r}'].number_format = 'dd mmm'
        yellow_blanks(ws, r, d['status'], {'E': 'open', 'F': 'open', 'G': 'done'})
        r += 1
    dv1 = DataValidation(type='list', formula1='"Not Started,In Progress,Blocked,Completed,Cancelled"', allow_blank=True)
    dv2 = DataValidation(type='list', formula1='"Urgent,High,Normal,Low"', allow_blank=True)
    ws.add_data_validation(dv1); ws.add_data_validation(dv2)
    dv1.add('B4:B400'); dv2.add('C4:C400')

# Master Rollup: keep the original master's ranking order
ws = wb.create_sheet('Master Rollup', 1)
set_widths(ws, {'A': 16, 'B': 30, 'C': 13, 'D': 11, 'E': 26, 'F': 34, 'G': 9, 'H': 9.5, 'I': 50, 'J': 46})
ws.freeze_panes = 'A4'
ws['A1'] = 'Master Rollup: all projects, ranked (Urgent, High, Normal, Low, done at bottom). Team = Viewer. Yellow = owner to fill.'
ws['A1'].font = F_NOTE
hdr_row(ws, 3, ['Owner'] + HDRS)
sm = src['Master Rollup']
full_to_tab = {v: k for k, v in OWNER_TABS.items()}
r = 4
i = 0
for row in sm.iter_rows(min_row=4):
    if row[0].value is None:
        continue
    owner, project, status, prio, kpi, summary = (row[0].value, row[1].value, row[2].value,
                                                  row[3].value, row[4].value, row[5].value)
    link = row[6].value if len(row) > 6 else None
    tab = full_to_tab[owner]
    key = (tab, project)
    vals = [owner, project, status, prio, kpi, IMPACTS.get(key, ''), DUES.get(key, ''),
            DELIVERED.get(key, ''), summary, link]
    write_project_row(ws, r, vals, status_col=3, banded=(i % 2 == 1))
    for col in ('G', 'H'):
        ws[f'{col}{r}'].number_format = 'dd mmm'
    yellow_blanks(ws, r, status, {'F': 'open', 'G': 'open', 'H': 'done'})
    r += 1; i += 1
dv1 = DataValidation(type='list', formula1='"Not Started,In Progress,Blocked,Completed,Cancelled"', allow_blank=True)
dv2 = DataValidation(type='list', formula1='"Urgent,High,Normal,Low"', allow_blank=True)
ws.add_data_validation(dv1); ws.add_data_validation(dv2)
dv1.add('C4:C400'); dv2.add('D4:D400')

# ------------------------------------------------------- KPI Targets H2
ws = wb.create_sheet('KPI Targets H2', 2)
set_widths(ws, {'A': 26, 'B': 12, 'C': 16, 'D': 8, 'E': 8, 'F': 8, 'G': 8, 'H': 8, 'I': 8, 'J': 10, 'K': 46})
title(ws, 'A1', 'KPI Targets H2 2026, per line (Tier 0 / Tier 1)')
note(ws, 'A2', 'Framework first: every target cell is a placeholder until agreed with Ivan. Bottom-up: current state -> diagnosis -> agreed actions -> estimated impact -> timeline. Yellow = set on the Ivan call or fill monthly (volumes: Jenny\'s dashboard; PBT: Nhat\'s model).')
MONTHS = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def targets_block(ws, r0, section, rows, fmt='#,##0'):
    ws.cell(row=r0, column=1, value=section).font = F_BLUEB
    hdr_row(ws, r0 + 1, ['Line', 'Phase', 'Owner'] + MONTHS + ['YTD att.', 'Basis / notes'])
    r = r0 + 2
    for line, phase, owner, notes in rows:
        t, a = r, r + 1
        ws.cell(row=t, column=1, value=line).font = F_BODYB
        ws.cell(row=t, column=2, value=phase).font = F_BODY
        ws.cell(row=t, column=3, value=owner).font = F_BODY
        ws.cell(row=a, column=1, value='   actual').font = F_NOTE
        for j in range(6):
            ct = ws.cell(row=t, column=4 + j)
            ca = ws.cell(row=a, column=4 + j)
            ct.number_format = fmt; ca.number_format = fmt
            ct.fill = FILL_FILL; ca.fill = FILL_FILL
        att = ws.cell(row=a, column=10,
                      value=f'=IFERROR(IF(COUNT(D{a}:I{a})=0,"-",SUM(D{a}:I{a})/SUMPRODUCT((D{a}:I{a}<>"")*D{t}:I{t})),"-")')
        att.number_format = '0%'; att.font = F_BODYB
        ws.cell(row=t, column=11, value=notes).font = F_NOTE
        ws.cell(row=t, column=11).alignment = WRAP
        for row_i in (t, a):
            for col in range(1, 12):
                ws.cell(row=row_i, column=col).border = THIN_BOT
        r += 2
    return r + 1

r = targets_block(ws, 4, 'Line outcomes, monthly volume (PHP M disbursement)', [
    ('QRPh disbursement', 'Star', 'Jastin', 'Run-rate target to confirm with Ivan. Hold and defend the star line (chargebacks, onboarding cycle time).'),
    ('Deals disbursement', 'Question', 'Anton + Manzil', 'Staged monthly ramp at positive NPM. Stage sizes and timing to agree; the reject-salvage plan sizes the ramp.'),
    ('Moto (KServico)', 'Question', 'JV', 'Run-rate target gated by Nhat\'s unit-economics check.'),
    ('Deals, managed accounts', 'Question', 'Manzil', 'ProTech, Maxicare, 3Cat. Ticket uplift target to agree.'),
])
r = targets_block(ws, r, 'Credit Line (utilization %, target set ~30 days post-launch)', [
    ('CL utilization / drawdown', 'New launch', 'Elias', 'Launched 15 Jul (F&F/ETB). Baseline first, then set the target with Ivan.'),
], fmt='0%')
r = targets_block(ws, r, 'Tier 0, PBT per line (PHP M, from Nhat\'s model)', [
    ('QRPh', 'Star', 'w/ Nhat', 'From Nhat\'s model once live.'),
    ('Online', 'Maintain', 'w/ Nhat', 'From Nhat\'s model once live.'),
    ('Moto / Deals', 'Question', 'w/ Nhat', 'Phase says push volume, watch NPM.'),
    ('Credit Line', 'New launch', 'w/ Nhat', 'Model rows live post-launch.'),
    ('Solar', 'Question', 'w/ Nhat', 'Kill or keep decision pending.'),
    ('Offline', 'Cash cow', 'w/ Nhat', 'Maintain, no PM by design.'),
])
ws.cell(row=r, column=1, value='Milestones (dates, not monthly numbers)').font = F_BLUEB
hdr_row(ws, r + 1, ['Milestone', 'Owner', 'Due', 'Done', 'Notes', '', '', '', '', '', ''])
mile = [
    ('Solar: kill-or-keep decision', 'Anton', None, 'Per KPI tab D3.'),
    ('CL utilization target set with Ivan', 'Elias + Kurt', dt.date(2026, 8, 15), '30 days post-launch.'),
    ('Card launch', 'Elias', None, 'Target Sep per KPI tab, prod Q4 2026 per Access Card row.'),
    ('PBT-per-line model live, monthly', 'Nhat', None, 'Reconciling to actuals.'),
    ('Metric-tree dashboard (Tier 1-3)', 'Jenny', None, 'One source for this tab.'),
]
r2 = r + 2
for m, o, due, n in mile:
    ws.cell(row=r2, column=1, value=m).font = F_BODYB
    ws.cell(row=r2, column=2, value=o).font = F_BODY
    cd = ws.cell(row=r2, column=3, value=due); cd.number_format = 'dd mmm'; cd.font = F_BODY
    if due is None:
        cd.fill = FILL_FILL
    cdn = ws.cell(row=r2, column=4); cdn.number_format = 'dd mmm'; cdn.fill = FILL_FILL
    ws.cell(row=r2, column=5, value=n).font = F_NOTE
    for col in range(1, 6):
        ws.cell(row=r2, column=col).border = THIN_BOT
    r2 += 1

# ------------------------------------------------------- KPI Key Drivers (carried over, numbers -> TBD)
ws = wb.create_sheet('KPI Key Drivers')
set_widths(ws, {'A': 18, 'B': 26, 'C': 40, 'D': 40, 'E': 40})
sk = src['KPI Key Drivers']
for row in sk.iter_rows(min_row=1, max_row=12, max_col=5):
    for c in row:
        if c.value is None:
            continue
        nc = ws.cell(row=c.row, column=c.column, value=c.value)
        if c.row == 1:
            nc.font = F_TITLE
        elif c.row == 2:
            nc.font = F_NOTE
        elif c.row == 4:
            nc.font = F_HDR; nc.fill = FILL_HDR
        else:
            nc.font = F_BODYB if c.column == 1 else F_BODY
            nc.border = THIN_BOT
            nc.alignment = WRAP
for coord, text in KD_OVERRIDES.items():
    ws[coord] = text
    if coord == 'A2':
        ws[coord].font = F_NOTE
    else:
        ws[coord].font = F_BODY
        ws[coord].border = THIN_BOT
        ws[coord].alignment = WRAP
ws.cell(row=14, column=1, value='Targets and monthly actuals live on the KPI Targets H2 tab. Delivery (D3) is scored by Kurt in the separate Delivery Scoreboard file.').font = F_NOTE
ws.freeze_panes = 'A5'

ORDER = ['README', 'Master Rollup', 'KPI Targets H2',
         'JV', 'Anton', 'Manzil', 'Elias', 'Jastin', 'KPI Key Drivers']
wb._sheets = [wb[n] for n in ORDER]
wb.save(OUT)
print('saved', OUT)
for s in wb.sheetnames:
    print(' ', s)

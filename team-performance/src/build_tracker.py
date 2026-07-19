#!/usr/bin/env python3
"""Build Executive_Project_Tracker_v2.xlsx from the original tracker.

Keeps the original structure and BillEase brand (white-dominant, blue 203AA9
headers, ink text, rationed color) and adds what Ivan's approach requires:
Impact / Due / Delivered columns, a Delivery Scoreboard, and a KPI Targets H2 tab.
"""
import datetime as dt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

SRC = 'tracker.xlsx'
OUT = 'Executive_Project_Tracker_v2.xlsx'

BLUE = '203AA9'
INK = '1A1A1A'
GRAY = '8A8A82'
BAND = 'F6F4EF'
FILLME = 'FFF3C9'   # yellow = cell for Kurt/PM to fill
WHITE = 'FFFFFF'

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
F_INPUT = Font(name='Arial', size=10, color='0000FF')  # hardcoded inputs
FILL_HDR  = PatternFill('solid', fgColor=BLUE)
FILL_BAND = PatternFill('solid', fgColor=BAND)
FILL_FILL = PatternFill('solid', fgColor=FILLME)
THIN_BOT = Border(bottom=Side(style='thin', color='D9D9D9'))
WRAP = Alignment(wrap_text=True, vertical='top')
TOP = Alignment(vertical='top')

OWNER_TABS = {'JV': 'JV Manlangit', 'Anton': 'Anton Betia', 'Manzil': 'Manzil Balani',
              'Elias': 'Elias Marcella', 'Jastin': 'Jastin Lagumbay'}

# --- seeded values: only facts already stated in the tracker/KPI tab/summaries ---
IMPACTS = {
    ('JV', 'Motorcycle Loans (KServico)'): 'Moto ~P15M/mo run rate (gated by Nhat)',
    ('Anton', 'Special Deals Offer to Low-Risk Customers'): 'Conversion lift on low-risk base - size w/ Nhat before comms',
    ('Manzil', 'Deals Merchant BD Pipeline'): 'New merchants live & disbursing; ticket uplift P1,000-2,000',
    ('Elias', 'Credit Line (Launch)'): 'CL utilization & drawdown - target set ~15 Aug (30d post-launch)',
    ('Elias', 'Access Card'): 'Per-card break-even on interchange @ CAC P300-500',
    ('Jastin', 'QRPh Chargeback Escalation (Netbank/AUB)'): 'Protects QRPh ~P107M/mo run rate',
    ('Jastin', 'Integrate Merchant Guide to Billease Docs'): '~30% fewer onboarding tickets',
}
DUES = {('Anton', 'Special Deals Offer to Low-Risk Customers'): dt.date(2026, 7, 20)}
DELIVERED = {
    ('JV', 'SAP Announcement & Quiz Module v1'): dt.date(2026, 7, 3),
    ('JV', 'Credit Line - Agent Announcement (SAP)'): dt.date(2026, 7, 16),
    ('Manzil', 'Maxicare PRIMA Launch on Deals'): dt.date(2026, 7, 10),
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
    ('B', 'One file. One tab per owner plus a consolidated Master. Linked to the PBT Metric Tree KPIs agreed with Ivan.'),
    ('S', ''),
    ('H', 'Purpose'),
    ('B', 'One row per project, straight to the point. ClickUp stays the main working document and source of truth.'),
    ('B', 'This sheet is the executive-level view: what the project is, whether it is moving, what it is expected to move (Impact), and whether we delivered when we said we would.'),
    ('S', ''),
    ('H', 'What is new in v2 (after the 29 Jun KPI alignment with Ivan)'),
    ('B', 'Impact (bottom-up): every project carries the estimated business impact and its assumption, e.g. "salvage ~20% of rejects -> +P6M/mo Deals disb". Targets come from agreed actions, never out of nowhere.'),
    ('B', 'Due and Delivered: the date agreed with the owner, and the date it actually shipped. This is the delivery track record Ivan asked for - delivery is managed by business result, not by number of emails sent.'),
    ('B', 'Delivery Scoreboard tab: per-owner on-time rate, computed automatically. This is each owner\'s D3 delivery KPI and the evidence base for the quarterly scorecard (Speed).'),
    ('B', 'KPI Targets H2 tab: the per-line volume and PBT targets, target vs actual by month. Yellow cells are to be agreed on the Ivan call or filled monthly from Nhat\'s PBT model and Jenny\'s dashboard.'),
    ('S', ''),
    ('H', 'The tabs'),
    ('B', 'Master Rollup: every project across all owners, ranked. Keep this Viewer-only for the team.'),
    ('B', 'KPI Targets H2: line-level targets (Tier 0/1) - review monthly.'),
    ('B', 'Delivery Scoreboard: delivery track record per owner - review weekly at standup.'),
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
    ('B', 'Weekly standup: walk the Master top-down - blocked and overdue first - and update Due/Delivered. Details live in ClickUp via the link column.'),
    ('B', 'Monthly: KPI readout on the KPI Targets H2 tab against Nhat\'s PBT-per-line model and Jenny\'s metric-tree dashboard.'),
    ('B', 'Quarterly: individual reviews on the QuantumLight (Revolut) Product Owner scorecard - Culture, Skills, and Deliverables = (Speed + Quality) x Complexity. The Delivery Scoreboard and Impact column are the evidence for Speed and business impact. A-players calibrated to 15-25% of the team.'),
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
    """rows: list of dicts with keys project,status,prio,kpi,summary,link"""
    out = []
    for d in rows:
        key = (tab, d['project'])
        d['impact'] = IMPACTS.get(key, '')
        d['due'] = DUES.get(key, '')
        d['delivered'] = DELIVERED.get(key, '')
        out.append(d)
    return out

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
    """vals: list aligned to columns starting at A."""
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
    """cols: dict letter->kind ('open' or 'done')"""
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
    ws['A1'] = f'{tab}: edit only this tab. Yellow = fill me (Impact & Due before In Progress; Delivered when shipped).'
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
    dv1.add(f'B4:B400'); dv2.add(f'C4:C400')

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

# ------------------------------------------------------- Delivery Scoreboard
ws = wb.create_sheet('Delivery Scoreboard', 2)
set_widths(ws, {'A': 18, 'B': 15, 'C': 11, 'D': 10, 'E': 8, 'F': 13, 'G': 13, 'H': 64})
title(ws, 'A1', 'Delivery Scoreboard, per owner (D3 delivery KPI)')
note(ws, 'A2', 'Ivan, 29 Jun: manage delivery by the track record of agreed steps shipped on pace, and by business impact, not activity. Computed from each owner tab (Due / Delivered / Status).')
hdr_row(ws, 4, ['Owner', 'Committed (Due set)', 'Delivered', 'On time', 'Late', 'Overdue (open)', 'On-time rate', 'Notes'])
r = 5
for tab, full in OWNER_TABS.items():
    ws.cell(row=r, column=1, value=full).font = F_BODYB
    ws.cell(row=r, column=2, value=f'=COUNT({tab}!F4:F400)')
    ws.cell(row=r, column=3, value=f'=COUNT({tab}!G4:G400)')
    ws.cell(row=r, column=4, value=f'=SUMPRODUCT(({tab}!G4:G400<>"")*({tab}!F4:F400<>"")*({tab}!G4:G400<={tab}!F4:F400))')
    ws.cell(row=r, column=5, value=f'=SUMPRODUCT(({tab}!G4:G400<>"")*({tab}!F4:F400<>"")*({tab}!G4:G400>{tab}!F4:F400))')
    ws.cell(row=r, column=6, value=f'=SUMPRODUCT(({tab}!F4:F400<>"")*({tab}!G4:G400="")*({tab}!B4:B400<>"Completed")*({tab}!B4:B400<>"Cancelled")*({tab}!F4:F400<TODAY()))')
    ws.cell(row=r, column=7, value=f'=IF(D{r}+E{r}=0,"-",D{r}/(D{r}+E{r}))')
    for col in range(2, 8):
        c = ws.cell(row=r, column=col); c.font = F_BODY; c.border = THIN_BOT
    ws.cell(row=r, column=7).number_format = '0%'
    ws.cell(row=r, column=1).border = THIN_BOT
    r += 1
ws.cell(row=r, column=1, value='Team').font = F_BLUEB
for col, letter in ((2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')):
    c = ws.cell(row=r, column=col, value=f'=SUM({letter}5:{letter}{r-1})'); c.font = F_BODYB
c = ws.cell(row=r, column=7, value=f'=IF(D{r}+E{r}=0,"-",D{r}/(D{r}+E{r}))')
c.font = F_BODYB; c.number_format = '0%'
r += 2
note(ws, f'A{r}', 'How to read it: Committed = rows with an agreed Due date. On-time rate = on time / (on time + late). Overdue (open) = past Due, not shipped, not cancelled.')
r += 1
note(ws, f'A{r}', 'Due is set when the step is agreed with the owner (standup or ClickUp), Delivered when it ships. Backfill both every Monday. Most rows are yellow today - first pass is due at the 21 Jul standup.')
r += 1
note(ws, f'A{r}', 'Feeds the quarterly Revolut-style scorecard: Speed <- on-time rate; Quality <- iterations to done (ClickUp reopens); Complexity <- precedent, judged per project. Deliverables = (Speed + Quality) x Complexity.')

# ------------------------------------------------------- KPI Targets H2
ws = wb.create_sheet('KPI Targets H2', 3)
set_widths(ws, {'A': 26, 'B': 12, 'C': 16, 'D': 8, 'E': 8, 'F': 8, 'G': 8, 'H': 8, 'I': 8, 'J': 10, 'K': 46})
title(ws, 'A1', 'KPI Targets H2 2026, per line (Tier 0 / Tier 1)')
note(ws, 'A2', 'Bottom-up targets: current state -> diagnosis -> agreed actions -> estimated impact -> timeline. Yellow = agree on the Ivan call, or fill monthly (volumes: Jenny\'s dashboard; PBT: Nhat\'s model).')
MONTHS = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def targets_block(ws, r0, section, rows, fmt='#,##0'):
    ws.cell(row=r0, column=1, value=section).font = F_BLUEB
    hdr_row(ws, r0 + 1, ['Line', 'Phase', 'Owner'] + MONTHS + ['YTD att.', 'Basis / notes'])
    r = r0 + 2
    for line, phase, owner, tgt, notes in rows:
        t, a = r, r + 1
        ws.cell(row=t, column=1, value=line).font = F_BODYB
        ws.cell(row=t, column=2, value=phase).font = F_BODY
        ws.cell(row=t, column=3, value=owner).font = F_BODY
        lbl = ws.cell(row=t, column=4)  # placeholder, replaced below
        # Target / Actual labels go in col A of a merged? keep simple: suffix rows
        ws.cell(row=a, column=1, value='   actual').font = F_NOTE
        for j, m in enumerate(MONTHS):
            ct = ws.cell(row=t, column=4 + j)
            ca = ws.cell(row=a, column=4 + j)
            ct.number_format = fmt; ca.number_format = fmt
            if tgt is not None:
                ct.value = tgt[j]
                ct.font = F_INPUT
                if tgt[j] is None:
                    ct.fill = FILL_FILL
            else:
                ct.fill = FILL_FILL
            ca.fill = FILL_FILL
        ca_first, ca_last = 'D', 'I'
        att = ws.cell(row=a, column=10,
                      value=f'=IFERROR(IF(COUNT({ca_first}{a}:{ca_last}{a})=0,"-",SUM({ca_first}{a}:{ca_last}{a})/SUMPRODUCT(({ca_first}{a}:{ca_last}{a}<>"")*{ca_first}{t}:{ca_last}{t})),"-")')
        att.number_format = '0%'; att.font = F_BODYB
        ws.cell(row=t, column=11, value=notes).font = F_NOTE
        ws.cell(row=t, column=11).alignment = WRAP
        for row_i in (t, a):
            for col in range(1, 12):
                ws.cell(row=row_i, column=col).border = THIN_BOT
        r += 2
    return r + 1

r = targets_block(ws, 4, 'Line outcomes, monthly volume (P M disbursement)', [
    ('QRPh disbursement', 'Star', 'Jastin', [107, 107, 107, 107, 107, 107], 'Run-rate ~P107M/mo per KPI tab; hold and defend (chargebacks, onboarding cycle time).'),
    ('Deals disbursement', 'Question', 'Anton + Manzil', [None] * 6, 'Staged P25M -> 50M -> 100M/mo at positive NPM; agree stage timing with Ivan. Salvage plan on rejects sizes the ramp.'),
    ('Moto (KServico)', 'Question', 'JV', [15, 15, 15, 15, 15, 15], '~P15M/mo, gated by Nhat\'s unit-economics check.'),
    ('Deals, managed accounts', 'Question', 'Manzil', [None] * 6, 'ProTech, Maxicare, 3Cat; ticket uplift P1,000-2,000.'),
])
r = targets_block(ws, r, 'Credit Line (utilization %, set ~15 Aug, 30d post-launch)', [
    ('CL utilization / drawdown', 'New launch', 'Elias', None, 'Launched 15 Jul (F&F/ETB). Baseline first, then set target with Ivan ~15 Aug.'),
], fmt='0%')
r = targets_block(ws, r, 'Tier 0, PBT per line (P M, from Nhat\'s model)', [
    ('QRPh', 'Star', 'w/ Nhat', None, 'May-26 read: small positive.'),
    ('Online', 'Maintain', 'w/ Nhat', None, 'May-26 read: possibly positive, small.'),
    ('Moto / Deals', 'Question', 'w/ Nhat', None, 'May-26 read: calculated negative; long-run unknown. Phase says push volume, watch NPM.'),
    ('Credit Line', 'New launch', 'w/ Nhat', None, 'Model rows live post-launch.'),
    ('Solar', 'Question', 'w/ Nhat', None, 'Kill-or-keep decision pending.'),
    ('Offline', 'Cash cow', 'w/ Nhat', None, 'Maintain; no PM assigned by design.'),
])
ws.cell(row=r, column=1, value='Milestones (dates, not monthly numbers)').font = F_BLUEB
hdr_row(ws, r + 1, ['Milestone', 'Owner', 'Due', 'Done', 'Notes', '', '', '', '', '', ''])
mile = [
    ('Solar: kill-or-keep decision', 'Anton', None, None, 'Per KPI tab D3.'),
    ('CL utilization target set with Ivan', 'Elias + Kurt', dt.date(2026, 8, 15), None, '30 days post-launch.'),
    ('Card launch', 'Elias', None, None, 'Target Sep per KPI tab; prod Q4 per Access Card row.'),
    ('PBT-per-line model live, monthly', 'Nhat', None, None, 'Reconciling to actuals.'),
    ('Metric-tree dashboard (Tier 1-3)', 'Jenny', None, None, 'One source for this tab.'),
]
r2 = r + 2
for m, o, due, done, n in mile:
    ws.cell(row=r2, column=1, value=m).font = F_BODYB
    ws.cell(row=r2, column=2, value=o).font = F_BODY
    cd = ws.cell(row=r2, column=3, value=due); cd.number_format = 'dd mmm'; cd.font = F_INPUT
    if due is None:
        cd.fill = FILL_FILL
    cdn = ws.cell(row=r2, column=4, value=done); cdn.number_format = 'dd mmm'; cdn.fill = FILL_FILL
    ws.cell(row=r2, column=5, value=n).font = F_NOTE
    for col in range(1, 6):
        ws.cell(row=r2, column=col).border = THIN_BOT
    r2 += 1

# ------------------------------------------------------- KPI Key Drivers (carried over)
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
ws.cell(row=14, column=1, value='Targets and monthly actuals live on the KPI Targets H2 tab. Delivery (D3) is scored on the Delivery Scoreboard tab.').font = F_NOTE
ws.freeze_panes = 'A5'

# order: README, Master, Delivery Scoreboard, KPI Targets H2, owners..., KPI Key Drivers
ORDER = ['README', 'Master Rollup', 'Delivery Scoreboard', 'KPI Targets H2',
         'JV', 'Anton', 'Manzil', 'Elias', 'Jastin', 'KPI Key Drivers']
wb._sheets = [wb[n] for n in ORDER]
wb.save(OUT)
print('saved', OUT)
for s in wb.sheetnames:
    print(' ', s)

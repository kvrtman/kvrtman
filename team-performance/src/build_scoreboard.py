#!/usr/bin/env python3
"""Build Delivery_Scoreboard.xlsx, Kurt's private delivery scoreboard.

Separate from the shared tracker on purpose: the team sees each other's work in
the tracker; individual delivery scores stay with Kurt. The Delivery Log tab
mirrors the tracker's Master Rollup columns exactly, so a weekly refresh is a
straight copy-paste (or IMPORTRANGE in Google Sheets).
"""
import datetime as dt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

SRC = 'Executive_Project_Tracker_v2.xlsx'
OUT = 'Delivery_Scoreboard.xlsx'

BLUE = '203AA9'
INK = '1A1A1A'
GRAY = '8A8A82'
BAND = 'F6F4EF'

F_TITLE = Font(name='Arial', size=13, bold=True, color=BLUE)
F_HDR   = Font(name='Arial', size=10, bold=True, color='FFFFFF')
F_BODY  = Font(name='Arial', size=10, color=INK)
F_BODYB = Font(name='Arial', size=10, bold=True, color=INK)
F_NOTE  = Font(name='Arial', size=9,  color=GRAY)
F_BLUEB = Font(name='Arial', size=10, bold=True, color=BLUE)
FILL_HDR = PatternFill('solid', fgColor=BLUE)
THIN_BOT = Border(bottom=Side(style='thin', color='D9D9D9'))

OWNERS = ['JV Manlangit', 'Anton Betia', 'Manzil Balani', 'Elias Marcella', 'Jastin Lagumbay']
LOG = "'Delivery Log'"

wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Scoreboard'
for col, w in {'A': 18, 'B': 15, 'C': 11, 'D': 10, 'E': 8, 'F': 13, 'G': 13, 'H': 64}.items():
    ws.column_dimensions[col].width = w

ws['A1'] = 'Delivery Scoreboard, per owner (D3 delivery KPI). Kurt only.'
ws['A1'].font = F_TITLE
ws['A2'] = 'Private file: individual delivery scores are not shared between team members. The shared tracker stays the team view of the work itself.'
ws['A2'].font = F_NOTE
ws['A3'] = 'Ivan, 29 Jun: manage delivery by the track record of agreed steps shipped on pace, and by business impact, not activity. Computed from the Delivery Log tab (Due, Delivered, Status).'
ws['A3'].font = F_NOTE

hdrs = ['Owner', 'Committed (Due set)', 'Delivered', 'On time', 'Late', 'Overdue (open)', 'On-time rate']
for i, h in enumerate(hdrs, start=1):
    c = ws.cell(row=5, column=i, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(vertical='center')
ws.row_dimensions[5].height = 21.75

r = 6
for owner in OWNERS:
    ws.cell(row=r, column=1, value=owner).font = F_BODYB
    ws.cell(row=r, column=2, value=f'=SUMPRODUCT(({LOG}!$A$4:$A$400=$A{r})*({LOG}!$G$4:$G$400<>""))')
    ws.cell(row=r, column=3, value=f'=SUMPRODUCT(({LOG}!$A$4:$A$400=$A{r})*({LOG}!$H$4:$H$400<>""))')
    ws.cell(row=r, column=4, value=f'=SUMPRODUCT(({LOG}!$A$4:$A$400=$A{r})*({LOG}!$H$4:$H$400<>"")*({LOG}!$G$4:$G$400<>"")*({LOG}!$H$4:$H$400<={LOG}!$G$4:$G$400))')
    ws.cell(row=r, column=5, value=f'=SUMPRODUCT(({LOG}!$A$4:$A$400=$A{r})*({LOG}!$H$4:$H$400<>"")*({LOG}!$G$4:$G$400<>"")*({LOG}!$H$4:$H$400>{LOG}!$G$4:$G$400))')
    ws.cell(row=r, column=6, value=f'=SUMPRODUCT(({LOG}!$A$4:$A$400=$A{r})*({LOG}!$G$4:$G$400<>"")*({LOG}!$H$4:$H$400="")*({LOG}!$C$4:$C$400<>"Completed")*({LOG}!$C$4:$C$400<>"Cancelled")*({LOG}!$G$4:$G$400<TODAY()))')
    ws.cell(row=r, column=7, value=f'=IF(D{r}+E{r}=0,"-",D{r}/(D{r}+E{r}))')
    for col in range(1, 8):
        c = ws.cell(row=r, column=col)
        if col > 1:
            c.font = F_BODY
        c.border = THIN_BOT
    ws.cell(row=r, column=7).number_format = '0%'
    r += 1
ws.cell(row=r, column=1, value='Team').font = F_BLUEB
for col, letter in ((2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')):
    c = ws.cell(row=r, column=col, value=f'=SUM({letter}6:{letter}{r-1})'); c.font = F_BODYB
c = ws.cell(row=r, column=7, value=f'=IF(D{r}+E{r}=0,"-",D{r}/(D{r}+E{r}))')
c.font = F_BODYB; c.number_format = '0%'

r += 2
for line in [
    'How to read it: Committed = rows with an agreed Due date. On-time rate = on time / (on time + late). Overdue (open) = past Due, not shipped, not cancelled.',
    'Refresh weekly: copy rows A4 down to J from the tracker\'s Master Rollup and paste into the Delivery Log tab (same columns). In Google Sheets, the Delivery Log tab can be replaced with IMPORTRANGE for auto-sync.',
    'Feeds the quarterly Revolut-style scorecard: Speed from the on-time rate, Quality from iterations to done (ClickUp reopens), Complexity judged per project. Deliverables = (Speed + Quality) x Complexity.',
]:
    ws.cell(row=r, column=1, value=line).font = F_NOTE
    r += 1

# ---------------- Delivery Log: exact mirror of Master Rollup ----------------
src = openpyxl.load_workbook(SRC)
sm = src['Master Rollup']
ws2 = wb.create_sheet('Delivery Log')
for col, w in {'A': 16, 'B': 30, 'C': 13, 'D': 11, 'E': 26, 'F': 34, 'G': 9, 'H': 9.5, 'I': 50, 'J': 46}.items():
    ws2.column_dimensions[col].width = w
ws2.freeze_panes = 'A4'
ws2['A1'] = 'Mirror of the tracker Master Rollup (columns A to J). Refresh by paste, or IMPORTRANGE in Google Sheets. The Scoreboard tab reads Owner (A), Status (C), Due (G), Delivered (H).'
ws2['A1'].font = F_NOTE
for i, h in enumerate(['Owner', 'Project', 'Status', 'Priority', 'KPI Key Driver', 'Impact (bottom-up)',
                       'Due', 'Delivered', 'Summary', 'ClickUp / BRD Link'], start=1):
    c = ws2.cell(row=3, column=i, value=h)
    c.font = F_HDR; c.fill = FILL_HDR; c.alignment = Alignment(vertical='center')
ws2.row_dimensions[3].height = 21.75
r = 4
for row in sm.iter_rows(min_row=4, max_col=10):
    if row[0].value is None:
        continue
    for i, c in enumerate(row, start=1):
        nc = ws2.cell(row=r, column=i, value=c.value)
        nc.font = F_BODY
        nc.border = THIN_BOT
        nc.alignment = Alignment(vertical='top')
        if i in (7, 8):
            nc.number_format = 'dd mmm'
    ws2.cell(row=r, column=1).font = F_BODYB
    r += 1

wb.save(OUT)
print('saved', OUT, 'log rows:', r - 4)

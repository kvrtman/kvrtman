#!/usr/bin/env python3
"""Update team_kpi.excalidraw with Ivan's feedback from the Jul call.

Keeps the existing three panels. Adds: who owns the numbers (panel 2), and the
delivery-first scoring model, seniority bar, initiative dimension and the
run-it-now todo (panel 3). Extends the separators to cover the new content.
"""
import json, random

SRC = 'team_kpi.excalidraw'
OUT = 'team_kpi.excalidraw'

INK = '#1e1e1e'
BLUE = '#203AA9'
AMBER = '#D9870B'
AMBER_BG = '#FCF0DC'

d = json.load(open(SRC))
els = d['elements']
UPD = max(e['updated'] for e in els)

def rid():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-') for _ in range(21))

idx_counter = [0]
IDX = ('b0g b0h b0i b0j b0k b0l b0m b0n b0o b0p b0q b0r b0s b0t b0u b0v b0w b0x b0y b0z '
       'b1A b1B b1C b1D b1E b1F').split()
def nidx():
    i = IDX[idx_counter[0]]; idx_counter[0] += 1
    return i

def text_el(x, y, text, color=INK, fs=20):
    lines = text.split('\n')
    w = max(len(l) for l in lines) * fs * 0.505
    h = len(lines) * fs * 1.25
    return {
        'id': rid(), 'type': 'text', 'x': x, 'y': y, 'width': round(w, 2), 'height': h,
        'angle': 0, 'strokeColor': color, 'backgroundColor': 'transparent',
        'fillStyle': 'solid', 'strokeWidth': 2, 'strokeStyle': 'solid', 'roughness': 1,
        'opacity': 100, 'groupIds': [], 'frameId': None, 'index': nidx(), 'roundness': None,
        'seed': random.randint(1, 2**31), 'version': 1, 'versionNonce': random.randint(1, 2**31),
        'isDeleted': False, 'boundElements': [], 'updated': UPD, 'link': None, 'locked': False,
        'text': text, 'fontSize': fs, 'fontFamily': 5, 'textAlign': 'left',
        'verticalAlign': 'top', 'containerId': None, 'originalText': text,
        'autoResize': True, 'lineHeight': 1.25,
    }

def rect_el(x, y, w, h, stroke, bg):
    return {
        'id': rid(), 'type': 'rectangle', 'x': x, 'y': y, 'width': w, 'height': h,
        'angle': 0, 'strokeColor': stroke, 'backgroundColor': bg, 'fillStyle': 'solid',
        'strokeWidth': 2, 'strokeStyle': 'solid', 'roughness': 1, 'opacity': 100,
        'groupIds': [], 'frameId': None, 'index': nidx(), 'roundness': None,
        'seed': random.randint(1, 2**31), 'version': 1, 'versionNonce': random.randint(1, 2**31),
        'isDeleted': False, 'boundElements': [], 'updated': UPD, 'link': None, 'locked': False,
    }

# ---- edit existing elements ------------------------------------------------
for e in els:
    # cadence text next to the calendar icon
    if e['id'].startswith('Li4JxnXK'):
        t = ('Weekly - tracker: due vs delivered, resyncs\n'
             'Monthly - numbers readout (context, not scoring)\n'
             'Quarterly - scorecard vs the bar → one score')
        e['text'] = t; e['originalText'] = t
        e['width'] = round(max(len(l) for l in t.split('\n')) * 20 * 0.505, 2)
        e['height'] = 75
        e['version'] += 1; e['versionNonce'] = random.randint(1, 2**31); e['updated'] = UPD
    # extend the two vertical separators to cover new content
    if e['id'].startswith('TwM2WEE_'):
        e['points'][-1] = [3.0, 1170]; e['height'] = 1170
        e['version'] += 1; e['versionNonce'] = random.randint(1, 2**31); e['updated'] = UPD
    if e['id'].startswith('Y4z7SMHk'):
        e['points'][-1] = [-5.5, 1210]; e['height'] = 1210
        e['version'] += 1; e['versionNonce'] = random.randint(1, 2**31); e['updated'] = UPD

new = []

# ---- panel 1 addition: tier 3 feeds the project list -----------------------
new.append(text_el(1995, 692,
    'Tier 3 = what we are doing to fix and balance → it becomes the project list',
    color=BLUE))

# ---- panel 2 additions: who owns the numbers --------------------------------
x2 = 3055
new.append(text_el(x2, 168, "Who owns the numbers (Ivan)", color=BLUE))
new.append(text_el(x2, 208,
    'Volume and PBT are management-owned: Ivan + Kurt + top mgmt define\n'
    'the numbers and choose the actions and projects to get there.'))
new.append(text_el(x2, 278, 'Do not punish the team for the number: they are not magicians.'))
new.append(text_el(x2, 323,
    "Volume-as-KPI is the network team's mood setter. Product is not sales:\n"
    'our end goal is profit, and sometimes less sales means more profit.'))
new.append(text_el(x2, 393, "The team's real impact = delivery of the projects we agreed."))

# ---- panel 3 additions: delivery-first scoring ------------------------------
x3 = 4090
new.append(text_el(x3, 150, 'Score the DELIVERY, not the number', color=BLUE))
new.append(text_el(x3, 190,
    'Speed - delivered on time? yes / no / faster\n'
    'Quality - delivered at the level expected, well thought through:\n'
    'every extra resync drops the quality automatically'))

new.append(text_el(x3, 295, 'The bar = seniority, not peers', color=BLUE))
new.append(text_el(x3, 335,
    '"I am not comparing you with him. I am comparing your bar with\n'
    'your performance." Junior / Mid / Senior is enough for our size.\n'
    'Juniors get a mistake discount; non-juniors: magic should happen.'))

new.append(text_el(x3, 440, 'Initiative = the 3rd dimension (growth, not bonus)', color=BLUE))
new.append(text_el(x3, 480,
    'Knows the numbers cold → connects problems to actions → brings\n'
    'initiatives. Assess each: easy or hard x high or low impact →\n'
    'it gets a priority → run it. A pure executor cannot grow.'))

new.append(rect_el(4072, 583, 706, 215, AMBER, AMBER_BG))
new.append(text_el(x3 + 8, 598, 'Do it NOW (my todo)', color=AMBER))
new.append(text_el(x3 + 8, 638,
    '1. Run the scorecard retro for the past 3 months, all 5 PMs.\n'
    '2. Do not wait for December; calibrate to one score: 5 4 3 2 1.\n'
    '3. Compare with gut feel; when it corresponds, adopt it.\n'
    '4. Replace the current general review with it; own the\n'
    '    process, do not leave it to HR.'))

els.extend(new)
json.dump(d, open(OUT, 'w'), separators=(',', ':'))
print('saved', OUT, '| elements:', len(els), '| added:', len(new))

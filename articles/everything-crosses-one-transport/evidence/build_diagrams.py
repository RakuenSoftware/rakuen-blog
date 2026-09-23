#!/usr/bin/env python3
"""Build source-grounded architecture SVGs and embed them in the article.

Run from any directory. Only derived diagrams and marked article blocks change.
Raw reporting artifacts are never read or written by this script.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / 'article/everything-crosses-one-transport.md'
OUT = ROOT / 'article/diagrams'
BLUE, INK, MUTED, LINE, AMBER = '#175b85', '#172d3b', '#526775', '#647985', '#965815'
PIN = 'https://github.com/RakuenSoftware/aimee/blob/6bcc87ea73f4e39947a5bc101d4033403b0e2324/'


def text(x, y, label, size=18, fill=INK, weight=400, anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>'


def box(x, y, w, h, title, lines=(), color='blue'):
    fill, stroke = {'blue': ('#eaf3f8', '#8daec3'), 'amber': ('#fff3df', '#cfa269'), 'white': ('#ffffff', '#b4c3cc')}[color]
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}"/>'
    out += text(x+16, y+29, title, 19, INK, 600)
    for i, line in enumerate(lines):
        out += text(x+16, y+57+i*25, line, 17, MUTED)
    return out


def arrow(points, key, dashed=False):
    d = 'M ' + ' L '.join(f'{x} {y}' for x,y in points)
    return f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2" marker-end="url(#{key}-arrow)"' + (' stroke-dasharray="6 5"' if dashed else '') + '/>'


def svg(key, h, title, desc, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {h}" width="720" height="{h}" role="img" aria-labelledby="{key}-title {key}-desc" style="display:block;width:100%;height:auto;min-width:620px;font-family:system-ui,-apple-system,sans-serif"><title id="{key}-title">{escape(title)}</title><desc id="{key}-desc">{escape(desc)}</desc><defs><marker id="{key}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{LINE}"/></marker></defs><rect width="720" height="{h}" rx="12" fill="#f7fafc"/>{body}</svg>'''


figures = []
k = 'bus-path'
b = text(28, 36, 'ONE DAEMON · ONE ORDERED ROUTE', 16, BLUE, 700)
b += box(28, 72, 190, 136, 'Module A', ('Own process', 'Outbound ring'))
b += box(502, 72, 190, 136, 'Module B', ('Own process', 'Inbound ring'))
b += '<rect x="246" y="60" width="228" height="346" rx="12" fill="#ffffff" stroke="#8daec3" stroke-dasharray="6 4"/>'
b += text(264, 88, 'C host', 19, INK, 600)
b += box(264, 106, 192, 60, 'Sequence stamp')
b += box(264, 202, 192, 60, 'Offer to tap')
b += box(264, 318, 192, 60, 'Route by grant')
b += arrow([(218,136),(264,136)],k)
b += arrow([(360,166),(360,202)],k)
b += arrow([(360,262),(360,318)],k)
b += arrow([(456,348),(488,348),(488,136),(502,136)],k)
b += box(28, 260, 190, 118, 'Capture sink', ('Frames + bodies', 'Can fail / prune'), 'amber')
b += arrow([(264,232),(238,232),(238,285),(218,285)],k)
b += text(360, 293, 'then', 16, MUTED, anchor='middle')
b += box(28, 436, 664, 92, 'Attach once over a Unix socket', ('Identity check → memory descriptors → mapped queues',), 'white')
b += text(28, 563, 'One direction shown. Replies use the reverse rings.', 17, MUTED)
b += text(28, 590, 'Core-local calls and cross-machine APIs sit outside this route.', 17, MUTED)
figures.append((k, svg(k, 616, 'Per-daemon transport and observation', 'Module A writes its outbound ring. The C host assigns a sequence, offers the event to the tap, then routes by grant into Module B’s inbound ring. Capture branches from the tap and can fail or be pruned. Unix attach passes memory descriptors once. This is an intra-daemon data path.', b),
    'Figure 1: The tap is upstream of routing. Persistence is a separate property of the sink. Queue direction is simplified to one request; each client has both rings.', 'docs/EVENT_BUS.md'))

k = 'delegate-egress'
b = text(28, 36, 'DELEGATED EXECUTION · MEDIATED EGRESS', 16, BLUE, 700)
b += box(28, 64, 664, 115, 'Delegate container · network none', ('Assigned worktree: writable for editing, read-only for review', 'No provider keys, forge credentials or Docker socket'))
b += arrow([(360,179),(360,222)],k)
b += text(380, 207, 'Unix control socket', 17, MUTED)
b += box(28, 222, 664, 89, 'aimee-server', ('Mediated tools: forge, web, memory, code index, providers',))
b += arrow([(360,311),(360,359)],k)
b += text(380, 341, 'package proxy request', 17, MUTED)
b += box(28, 359, 664, 110, 'Go-owned proxy', ('Check host + port → resolve → validate IP → dial that IP', 'Plain HTTP: filter headers. CONNECT: relay opaque bytes.'))
b += arrow([(360,469),(360,515)],k)
b += box(28, 515, 664, 62, 'Allowed package destination', (), 'white')
b += box(28, 608, 664, 89, 'Verify actual state before handover', ('Inspect network, mounts and environment on start or resume.',), 'amber')
b += text(28, 733, 'Failure or unknown state refuses the container.', 17, MUTED)
figures.append((k, svg(k, 759, 'Delegate network boundary and package proxy', 'The container has no direct external network route. A mounted Unix control socket reaches mediated tools in aimee-server. Package requests use the Go proxy, which validates a destination before dialing. Post-start and resume checks inspect actual network, mounts and environment. The source worktree is also a mounted data surface.', b),
    'Figure 2: The package path is expanded; other mediated tools have their own handlers. The worktree remains a data surface. This describes the enabled sandbox posture, not an escape test.', 'docs/DELEGATE_SANDBOX.md'))

k = 'witness-chain'
b = text(28, 36, 'MEMORY EVIDENCE · TWO TRANSACTIONS', 16, BLUE, 700)
b += box(28, 65, 664, 113, '1. Mutation transaction', ('Change memory + insert immutable outbox intent', 'Intent submission failure aborts the mutation.'))
b += arrow([(360,178),(360,233)],k)
b += text(380, 211, 'commit', 17, MUTED)
b += box(28, 233, 664, 90, 'Committed intent waits for the worker', ('Memory is committed; the completed witness may lag.',), 'amber')
b += arrow([(360,323),(360,379)],k)
b += text(380, 354, 'bounded drain', 17, MUTED)
b += box(28, 379, 664, 139, '2. Worker transaction · separate credential', ('Append chain row + witness + delivery acknowledgement', 'Commit all together.', 'Failure rolls back the drain; the intent remains pending.'))
b += arrow([(360,518),(360,571)],k, True)
b += text(380, 549, 'export + retain', 17, MUTED)
b += box(28, 571, 664, 89, 'Off-host evidence consumer', ('Useful only for records and checkpoints it actually retains.',), 'white')
b += text(28, 696, 'Dashed arrow: retention depends on operator configuration.', 17, MUTED)
b += text(28, 723, 'Bus capture is a separate record and does not seal this chain.', 17, MUTED)
figures.append((k, svg(k, 749, 'Asynchronous memory witness pipeline', 'The memory mutation and immutable outbox intent commit in one transaction. A separately credentialed worker later appends the hash-chain row, witness and delivery acknowledgement in a second transaction. Failure of that drain rolls it back for retry. Off-host retention depends on a configured consumer. Bus capture is separate.', b),
    'Figure 3: A durable intent closes the gap at mutation commit; chain construction follows asynchronously. The validation report tests worker rollback and idempotent restart.', 'docs/validation/memory-changeset-worm-seal-2026-08-25.md'))

k = 'service-split'
b = text(28, 36, 'SERVICE SPLIT · SEPARATE AUTHORITY AND RECORDS', 16, BLUE, 700)
b += box(28, 66, 294, 210, 'aimee-server', ('Near one user’s work', 'Can invoke local tools', 'Own bus + grants', 'Own records'))
b += box(398, 66, 294, 210, 'aimee-kb', ('Shared learned state', 'Memory + policy decisions', 'Own bus + grants', 'Evidence ledger + worker'))
b += arrow([(322,137),(398,137)],k)
b += text(360, 121, 'request', 14, MUTED, anchor='middle')
b += arrow([(398,209),(322,209)],k)
b += text(360, 194, 'reply', 14, MUTED, anchor='middle')
b += text(28, 472, 'The link between services is an authenticated network API.', 17, MUTED)
b += text(28, 498, 'Each service’s shared-memory bus stays inside its daemon.', 17, MUTED)
b += arrow([(175,276),(175,315),(260,315),(260,350)],k, True)
b += arrow([(545,276),(545,315),(460,315),(460,350)],k, True)
b += box(28, 350, 664, 89, 'Retained exports', ('Comparison is possible where independent copies survive.',), 'white')
b += box(28, 533, 664, 113, 'Either side can cause harm', ('Server compromise: reachable work and credentials.', 'KB compromise: false memory or policy in replies.'), 'amber')
b += text(28, 682, 'Dashed arrows depend on export and retention configuration.', 17, MUTED)
b += text(28, 709, 'Independent processes do not guarantee independent hosts.', 17, MUTED)
figures.append((k, svg(k, 735, 'Server and knowledge-base service topology', 'A user’s server initiates requests to a shared knowledge base, which replies. Each daemon has its own intra-daemon bus, grants and records. Authenticated network APIs connect the services. Configured exports may provide independent retained records. Either service can cause harm on its own; no automatic mutual-audit routine is established.', b),
    'Figure 4: One server and one KB are shown; several servers can use the KB. Separate records permit reconciliation. Physical and administrative separation depend on deployment.', 'docs/EVENT_BUS.md'))

body = ARTICLE.read_text()
OUT.mkdir(exist_ok=True)
for key, drawing, caption, source in figures:
    (OUT / f'{key}.svg').write_text(drawing+'\n')
    figure = f'<figure class="sg-figure"><div role="region" aria-label="{key.replace("-", " ")} diagram, scroll horizontally on small screens" tabindex="0" style="overflow-x:auto">{drawing}</div><figcaption class="sg-figure__caption">{escape(caption)} <a href="{PIN+source}">Source at the audited revision</a>.</figcaption></figure>'
    pattern = rf'<!-- diagram:{key} -->.*?<!-- /diagram:{key} -->'
    body, count = re.subn(pattern, f'<!-- diagram:{key} -->\n{figure}\n<!-- /diagram:{key} -->', body, flags=re.S)
    if count != 1:
        raise ValueError(f'Expected one marker pair for {key}, got {count}')
ARTICLE.write_text(body)
print(f'Built and embedded {len(figures)} diagrams.')

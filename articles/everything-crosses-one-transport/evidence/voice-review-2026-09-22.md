# Voice pass, 2026-09-22

## Scope and pre-edit inventory

Input: the restored article at blog commit `d0e2b9c`. Guide:
[JBailes/voice-guide](https://github.com/JBailes/voice-guide/tree/6cb3dc0762b4b17e5d61a99a30086a3806945e27),
VOICE.md Parts I and III and ARTICLE.md Part I. The author requested the
identified voice edits and excluded the separately discussed factual corrections.
The architecture essay remains the organising form. This pass introduces no
runtime measurement, source re-audit or new implementation claim.

Inventory recorded before editing. The 45-item inventory in
[the September 20 review](editorial-review-2026-09-20.md#inventory-made-before-editing)
is useful as an index of the same source article. Its rewrite dispositions
remain superseded; this pass does not adopt them. The dispositions below govern
this edit. Historical reporting and raw artifacts remain unchanged.

| Prior reporting | Class | Disposition in this pass |
| --- | --- | --- |
| Product identity, hosting choices, scope and scale | Author positioning and shared document review | Retain orientation after the opening finding; retain disclosure. |
| Two-in-the-morning goal, defaults and configuration choices | Author design intent | Retain goal and configuration mechanism; consolidate repeated rationale. |
| 134 ns, 16-byte dispatch; 117 ns controlled enqueue; eight runs of 5,000 emits | First-party measurements reported in the baseline | Retain figures, conditions and median/bound distinction unchanged. |
| Both 1,000 ns ceilings and merge gate | Source/document review | Retain unchanged. |
| i7-14700K, Go 1.24.4 cgo ranges and eight-pointer case | Previously reported first-party comparison | Retain paragraph unchanged; factual correction excluded by author. |
| Other transports' tail behaviour and named causes | Author investigation, without published candidate measurements | Retain account; do not promote it to a comparative benchmark. |
| C/Rust choice; C and pure-Go clients; conformance and no cgo | Author design account and source/document review | Retain; explain language independence once. |
| Ring pairs, attach checks, memfd/SCM_RIGHTS, arena trust, fragmentation and 16 MiB limit | Source/document review | Retain every mechanism and scope condition. |
| LMAX, virtio, io_uring, DPDK, Aeron and seL4 | Author prior-art reading | Retain all names and scoped novelty judgment. |
| Learning grant; permanent references; fail-closed learning, memory and governance | Grant/source/document review | Retain examples and limits. |
| Model's unused-node/testing-key incident | Author-reported self-learning observation | Retain incident unchanged; no billing measurement or reproduction inferred. |
| Network-none curl check, socket mediation, proxy policy, numeric destination and credential removal | Deployment/source/document review | Retain checks, figures, policy and destination account. |
| Hosted-provider tool configuration and lack of all-provider e2e coverage | Configuration review and reporting limit | Retain unchanged. |
| Mediated git prerequisite and recall/egress relationship | Author implementation account and unmeasured design inference | Retain prerequisite, missing longitudinal measurement and recall failure condition. |
| Start/resume inspection, opt-out and PR 2839 | Source/document review and recorded merge check | Retain all checks, switch and link. |
| Authentication owners, downstream verification and four-kind sandbox grant | Source/document review | Retain; remove only a repeated general OS-authority explanation. |
| Pre-routing tap, monotonic order, retries, overflow, producer_reaped and control_lost | Routing source/document review | Retain mechanisms; consolidate repeated explanation of actor-independent observation. |
| 5,000 audit intents and zero duplicate/drop after shutdown | First-party durability result | Retain number, fixture and shutdown scope unchanged. |
| WORM, source/witness transaction, C and five SQL close paths, restart and recovery | Prior source review and first-party validation report | Retain paragraph unchanged; factual correction excluded by author. |
| Ed25519 checkpoints, local tamper checks, off-host copies and unreconstructable gaps | Runbook review and security analysis | Retain mechanism and all distinct retention/recovery limits; consolidate repetition. |
| Server/KB roles, multiplicity, isolation and initiation asymmetry | Deployment/source review and author analysis | Retain argument; consolidate repeated plugin-authority qualification and final recap. |
| Four learning components stranded across the boundary | Shared first-party testing and build-graph review | Retain incident, count and link. |

No interview, independent benchmark or new vendor report is introduced. No prior
first-party reporting is dropped. Cuts remove repeated explanation or move an
existing point to its first useful position.

## Completed edit

The opening now leads with the transport constraint, then supplies project
orientation and the operational goal. Repeated language-independence, plugin
authority, observation and retention explanations are consolidated. The
ending names the operator's grant, sandbox and export-retention choices. The
article remains an architecture essay, with its original section sequence.

Whitespace-delimited word count, including frontmatter: 5,398 to 4,795
(603 words removed). The cut follows repeated explanation rather than a
percentage quota. The author's dry line about defaults waking their own team
remains. Both excluded factual passages are byte-for-byte unchanged.
All source URLs and distinct numeric tokens remain. All 29 raw files
match their pre-edit SHA-256 hashes. No historical reporting file was replaced.

The repository voice gate and `git diff --check` both pass.

# Figure provenance and reporting record

The argument here is about protocol shape and the evidence for it is one
benchmark table. That table does not currently reproduce, and the way it fails
bears on the article's thesis rather than on its arithmetic.

## Where the table comes from

The figures match the run recorded at 2026-08-11 22:00: all runs on one image
`sha256:239f6b3e`, task `t01_cache`, three replicates, economizer attached and
aggressive. Baseline credits there were 4.48, 5.24 and 5.62 for a mean of 5.11,
which is the article's baseline credit figure, and input 68k to 116k, which
brackets its 91k.

**Those cells are not on this machine.** They were run on CT403 and nothing under
either benchmark tree was written after that deploy. So none of the four columns
has been re-derived here.

## The credits column is measured on a thrashing host

On 2026-08-12 CT403 was found at load 89 with 93 tasks in uninterruptible sleep.
The cause was `aimee-server` anonymous memory at about 20 GB, which left the
kernel no reclaimable file cache and set it re-reading the executables at roughly
860 MB/s. The author's note on it says plainly that benchmark timings and credits
measured on that box while thrashing are suspect, including the 22:00 run.

Token counts and call counts are protocol facts and do not move with page-cache
thrash. Credits and wall time do. The article says so in the text and leans on
tokens and calls, which is the right division, and the credits column should not
be quoted on its own.

## The committed measurement of the same task disagrees

`articles/three-zeros-and-a-wrong-answer/benchmarks/ct403-results/` holds three
`t01_cache` replicates per run for the same comparison, committed and verified.
Recomputed from those cells:

| | baseline | ours | ratio |
|---|---:|---:|---:|
| input tokens | 93,321 | 544,234 | 5.83× |
| `agent_message` | 4.3 | 7.0 | 1.63× |
| tool calls | 12.0 | 25.3 | 2.11× |
| messages plus tool calls | 16.3 | 32.3 | 1.98× |

The article gives 8.7 against 29.0 calls and 91k against 389k tokens. Baseline
tokens agree at 91k against 93k. Nothing else does: the committed cells put our
input at 544k rather than 389k, and no call metric in them yields 8.7 or 29.0.

The likely reason the two runs differ on tokens is that the 22:00 run had the
economizer attached and aggressive and the committed campaign did not. That is a
configuration difference rather than noise, and it means the two must not be
mixed in one table.

### The disagreement is about the thesis

Both runs put the total gap near 4× to 6×, and they split it in opposite ways.

| basis | round trips | per-call weight |
|---|---:|---:|
| the article, calls | **3.3×** | 1.27× |
| committed cells, messages plus tool calls | 1.98× | **2.94×** |
| committed cells, `agent_message` only | 1.63× | 3.58× |

The article's case is that round trips dominate and per-call weight is the
smaller term. On the committed cells that reverses under every unit tested.

This is not a rounding dispute. It decides which sentence the article is allowed
to end on, and it turns entirely on what counts as a turn. A tool result forces a
fresh model request, so tool calls are closer to billed turns than assistant
messages are, which argues for the article's unit. That case has to be made in
the text rather than assumed, because the choice of denominator is the argument.

`articles/three-zeros-and-a-wrong-answer/evidence/figures.md` records a third
decomposition, 1.42× trips against 2.93× weight, on the `agent_message` basis
across all tasks. Three numbers for one quantity is a sign the quantity is not yet
defined.

## Not yet cited

| figure | status |
|---|---|
| 2.2 to 3.0 times more expensive | consistent with the 22:00 credits, and those credits are the suspect column |
| identical hidden-test results in every cell | the 22:00 note records `hidden_ok` true, `compile` 0 and `smoke` 0 across all nine cells. Not re-checked here |
| about 178k of 389k input tokens are conversation re-sends | not cited, and not derivable from a cell summary |
| zero command-line invocations across thirteen cells | not cited. `tool_calls` in the committed cells records `command_execution` counts but not which command ran, so this needs the transcripts |
| nineteen tools | not cited |
| four capabilities that exist only as tools | not cited |
| four attempts to move the behaviour by wording | not cited |

The handshake quotation is verbatim from the MCP initialize message and is the
one piece of evidence here that needs no artifact beyond the server itself.

## Reporting inventory and disposition

- **The comparison of surfaces:** kept. It is an argument about what the protocol
  can express, not a measurement, and it stands on the absence of an `&&`.
- **The cost table:** kept and flagged. It is the article's only measurement and
  it does not reproduce against the committed campaign.
- **The credits column:** kept, marked indicative in the text, and not to be
  quoted alone.
- **The handshake finding:** kept. It is a source audit of our own configuration
  and needs no run.
- **Adjacent interest:** disclosed in the article, next to the claim, and the
  layer that comes off worst is ours.

## What has to happen before this can be published

1. Commit the 22:00 cells, or rerun the comparison on a quiet host and use that.
2. Settle what counts as a turn, and say so in the text. The decomposition
   reverses depending on the answer, and the article's conclusion rides on it.
3. Decide whether the economizer was attached, and state the configuration.
4. Cite the re-send figure, the tool count, the four tool-only capabilities and
   the four wording attempts.
5. Establish the zero command-line invocations from the transcripts, since it is
   a zero and this series has been caught by those repeatedly.

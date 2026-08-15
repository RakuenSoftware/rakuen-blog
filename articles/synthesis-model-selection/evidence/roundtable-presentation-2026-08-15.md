# Roundtable review: published presentation

The published `synthesis-model-selection` article received three independent,
read-only review passes on August 15, 2026. The review covered the completed
six-figure presentation, its Numbers tabs, the canonical analysis and the
article's adherence to `/home/virant/dev/voice-guide/VOICE.md`.

The article retains its original publication date, measurements, findings and
recommendation. This review concerns presentation completion using the same
canonical analysis.

## Data and provenance

The data reviewer returned no findings after checking all six figures against
`canonical/analysis-20260815.json`. The displayed scores, latency and memory
measurements, paired ranges, task-level point estimates, output totals, decode
rates and completeness rates reconcile with the source. Derived percentages,
the five-point content-latency frontier and the canonical SHA-256 also match.

A final integrity pass confirmed that the presentation and wording work did not
alter a displayed value, comparison direction, qualification or recommendation.

## Voice and claim calibration

The voice reviewer identified and resolved wording that was stronger than the
measurements supported, repetition in the Qwen3.8 latency explanation, two
unexpanded terms and several imprecise headings or antecedents. The final pass
returned no findings and signed off the article against Parts I and III of
`VOICE.md`.

The article continues to distinguish observed task leaders from paired model
selection, treats ranges crossing zero as a failure to detect a difference and
does not present that outcome as equivalence.

## Rendering and interaction

The rendering reviewer checked six Chart/Numbers pairs, twelve unique radio
identifiers, labels and controls, SVG bounds, accessible chart labels and raw
number coverage. Five presentation findings were resolved:

- The content-latency frontier now uses a distinct dashed line and a legend
  that matches the point colours.
- Two nearly coincident frontier points retain their exact coordinates but use
  leader lines, translucent fills and a dashed outline to remain legible.
- The paired-comparison chart gives zero the established decision-rule style.
- Muse's completion-token label sits outside its bar.
- The completeness chart explains its point colours.

The final rendering pass returned no findings.

## Independent checks

- `validate_article_figures.py`: six complete Chart/Numbers figures and all
  canonical values present.
- `python3 tools/voice_gate.py synthesis-model-selection`: pass.
- `python3 -m unittest tools.test_voice_gate -v`: two tests passed.
- Python compilation for every `benchmarks/ab-v2/*.py` file: pass.
- `git diff --check`: pass.
- Website TypeScript check: pass.
- Website tests: four tests passed.
- Website production build: pass.
- Rendered Markdown audit: six figures, six SVG charts, six tables, six Chart
  tabs and six Numbers tabs.

The roundtable signed off the completed published presentation with no
remaining findings.

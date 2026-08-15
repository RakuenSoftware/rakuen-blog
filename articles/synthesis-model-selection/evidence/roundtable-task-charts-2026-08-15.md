# Roundtable review: full task charts

The published `synthesis-model-selection` presentation received three
independent, read-only review passes on August 15, 2026 after its combined task
chart was replaced with five task-specific Chart/Numbers figures.

The opening now explains the task score and tested serving configurations,
then presents Claim, Code Unit, Document Summary, Entity and Synthesis before
the overall ladder and the rest of the analysis. Each task figure shows all
nine tested configurations in both views.

## Data and provenance

The data reviewer checked all 45 chart values and all 45 Numbers cells against
`canonical/analysis-20260815.json`. Every task uses the correct descending
order, observed leader and zero-based scale:

- Claim: zero to 0.25 F1; Gemma 4 31B led at 0.2393.
- Code Unit: zero to 0.50 F1; Gemma 4 31B led at 0.4758.
- Document Summary: zero to 0.50 F1; Gemma 4 12B led at 0.4891.
- Entity: zero to 0.15 F1; Gemma 4 26B-A4B led at 0.1395.
- Synthesis: zero to 0.50 F1; Qwen3.8 27B led at 0.4920.

The reviewer also confirmed that the serving-configuration paragraph matches
the canonical metadata and appears before the task charts. The final pass
returned no findings.

## Voice and calibration

The voice review retained the requested task-chart-first order and tightened
the explanation around it. The article now counts four distinct leaders across
five tasks, warns that the charts use different horizontal scales and uses the
established term “paired range” in every caption. It does not turn descriptive
task ordering into model-selection claims.

The final review against Parts I and III of
`/home/virant/dev/voice-guide/VOICE.md` returned no findings.

## Rendering and interaction

The rendering reviewer confirmed that each task Chart and Numbers tab contains
nine unique model rows with matching values. Labels and printed values remain
inside their 760-pixel view boxes without collisions. All ten article figures
have unique radio identifiers, complete label/control wiring and accessible SVG
labels. The five task figures precede the overall ladder.

The final rendering pass returned no findings.

## Independent checks

- `validate_article_figures.py`: ten complete Chart/Numbers figures and all
  canonical values present.
- `python3 tools/voice_gate.py synthesis-model-selection`: pass.
- `python3 -m unittest tools.test_voice_gate -v`: two tests passed.
- Python compilation for every `benchmarks/ab-v2/*.py` file: pass.
- `git diff --check`: pass.
- Website TypeScript check: pass.
- Website tests: seven tests passed.
- Website production build: pass.
- Rendered Markdown audit: ten figures, ten SVG charts, ten tables, ten Chart
  tabs and ten Numbers tabs; the task figures precede the overall ladder.

The roundtable signed off the full task-chart presentation with no remaining
findings.

---
title: "Quantization Choice Mattered More Than Bit Count"
date: 2026-08-09
author: Rakuen Software
tags: [quantization, local-models, benchmarks, aimee]
excerpt: "Two of five bit-width steps cleared their paired range, and neither was a step up from four bits. Quantization-aware training mattered most by moving a 26B model onto a 16-gibibyte card."
---

*Rakuen builds aimee, the system measured here. Every run and incomplete rerun is
listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/which-quant-beats-how-many-bits/evidence/figures.md).*

Two of five bit-width comparisons separated within their own paired ranges, and
neither was a plain step up from four bits. A dynamic four-bit packing led a flat
four-bit build by 0.0229 on the harmonic mean of precision and recall (F1), but
that pair crossed hardware and cannot yet support the mechanism claim.
Quantization-aware training (QAT) mattered most by moving a 26B model onto a
16-gibibyte card.

All paired bootstrap ranges resample notes rather than facts. Each range below
was produced in its own process, one comparison per invocation, because the
scorer draws its individual and paired intervals from a single random stream and
a third run shifts a paired endpoint.

## Two of five bit-width steps separated

| comparison | difference | 95% range |
|---|---:|---:|
| gemma-4-E2B, Q6 minus Q4 | +0.0065 | −0.0142 to +0.0273 |
| gemma-4-E4B, Q6 minus Q4 | +0.0150 | −0.0035 to +0.0339 |
| gemma-4-E4B, Q6 minus Q8 | **+0.0245** | **+0.0091 to +0.0405** |
| SmolLM3-3B, Q8 minus Q4 | **+0.0351** | **+0.0156 to +0.0543** |
| LFM2.5-2.6B, Q4 minus Q8 | +0.0104 | −0.0153 to +0.0363 |

The two that separated point opposite ways on bit count. SmolLM3-3B gained from
eight bits over four, and it is the weakest model in the set at 0.3933. At E4B,
six bits beat eight: 0.6339 against 0.6094, a step *down* in width that scored
better.

The 10,000-note Gemma ladders agree. E2B scored 0.6246, 0.6344 and 0.6329 across
Q4, Q6 and Q8; E4B scored 0.6301, 0.6452 and 0.6337. Both peak at six bits and
fall back at eight, so more bits did not provide a consistent direction.

An earlier claim that LFM2.5 worsened with more bits is withdrawn because its
range crosses zero.

The E2B Q6-minus-Q4 direction was positive in eight runs across five related
corpora. A sign test under independent, equally likely directions gives 0.008.
Those runs share prompt, scorer and generator lineage, so independence does not
hold and 0.008 is an optimistic bound. Three repeats of one configuration were
byte-identical on all 1,001 notes, showing that ordinary rerun drift did not
produce the repeated direction.

## QAT improved the smallest model's score

| size | QAT minus non-QAT | 95% range |
|---|---:|---:|
| E2B | **+0.0389** | **+0.0152 to +0.0635** |
| E4B | about 0 | not reported |
| 12B | +0.0100 | −0.0091 to +0.0289 |
| 31B | +0.0108 | −0.0013 to +0.0235 |

Only E2B supports an accuracy benefit within its reported range. The two larger
differences point in the same direction but do not separate. The data do not
establish a size trend or show why any effect changes with size.

## The dynamic four-bit build needs a same-card rerun

Google's QAT build used flat `q4_0` packing. Unsloth repacked the same trained
weights with a dynamic scheme that assigns tensor formats by sensitivity.

| 26B-A4B run | F1 | precision | recall | parsed |
|---|---:|---:|---:|---:|
| Unsloth QAT dynamic | **0.6804** | 0.6501 | 0.7136 | 958 of 1,001 |
| Google QAT flat `q4_0` | 0.6575 | 0.6398 | 0.6761 | 940 of 1,001 |

The difference was **+0.0229**, with a 95% range from **+0.0022 to +0.0440**.
The runs used different hardware. A rented-versus-local calibration had about
±0.019 uncertainty at 1,001 notes, nearly covering the lower edge. The result is
a candidate packing effect, not evidence that the packer beat the training.

## QAT changed the hardware tier

| model | QAT file | non-QAT file |
|---|---:|---:|
| gemma-4-26B-A4B UD-Q4 | **13.27 GiB** | 15.84 GiB |
| gemma-4-31B UD-Q4 | 16.10 GiB | 17.53 GiB |

The RTX 5080 had 15.92 gibibytes free after server startup. The QAT 26B fit with
its draft head; the non-QAT build did not. The QAT run reached 323 tokens per
second and scored 0.6804. Several file and resident-memory figures are
single-sourced in server logs and article notes rather than a dedicated size
artifact.

On a matched 12B speed probe, QAT reached 285.7 tokens per second and non-QAT
233.1, a 22.6% difference. Draft acceptance was 85.4% and 84.2%, respectively.
The files differed by 9% in size.

A tensor-format explanation remains unverified.
The same model varied from 84.4 to 131.9 tokens per second across five rented hosts,
so only the same-card comparison supports the speed difference.

## Speculative acceptance stayed within one point per pair

| pair | non-QAT or flat | QAT or dynamic |
|---|---:|---:|
| 12B | 82.0% of 1,510,235 drafted tokens | 81.2% of 1,414,986 |
| 26B | 79.1% of 1,367,766 | 79.2% of 1,360,556 |
| 31B | 78.5% of 620,046 | 79.1% of 539,715 |

The observed acceptance rates moved by less than one percentage point inside each
pair, even where F1 differed. In these runs, quantization choice and speculative
decoding did not show a material interaction. That is a measurement over three
pairs, not a general composability rule.

## Parse failures bounded two comparisons

The two 12B runs parsed 90% and 92% of answers, with no context exhaustion. Their
scores are floors because malformed JSON counted as failure.

For E2B, scoring only rows parsed by the worse run moved the difference by −0.0028.
Perfectly repairing all 40 unreadable rows could add at most **+0.0038** because
they held 15 gold facts and 26 factless notes. The two corrections moved in
opposite directions and remained inside the paired range. The equivalent repair
bound has not been computed for 12B.

## Choose a quantization by the decision it changes

At E2B, Q4 saves 1.4 gibibytes while the Q6 difference is small and reverses under
a relation-agnostic score by 0.0052. At E4B, Q6 is the one width choice here that
cleared its range: it leads strict and relation-agnostic F1, improves abstention
and emits seven fewer spurious triples, and it beats the wider Q8 build rather
than losing to it. At 12B and above, no accuracy difference here cleared its
range, so fit and measured throughput carry more weight.

Check for a QAT build before buying a larger card. Treat the 26B dynamic packing as
a same-card test candidate, not a recommendation. Report parse floors beside the
headline score.

All ladders share one corpus lineage. The 12B, 31B and 26B pairs also crossed
machines. Registered 3,002-note same-card reruns for 12B and 31B produced no
complete prediction files and contribute no result. A second independently built
corpus and completed same-card pairs are the gates for stronger claims.

---
title: "Local LLMs: Speculative Decoding"
date: 2026-08-06
author: Rakuen Software
tags: [benchmarks, local-models, speculative-decoding, throughput, aimee]
excerpt: "Eleven matched pairs made Gemma and Qwen faster without a resolved accuracy change. Muse Glimmer then showed why the exact model, draft and backend still have to be tested."
---

Eleven same-card pairs made Gemma and Qwen **1.65x to 2.54x faster** without a
resolved accuracy change. Then Muse Glimmer's vendor-supplied DFlash drafter made
our RX 7900 XTX **9% slower**. The feature did not change. The model, draft and
backend did.

That is the result. Speculative decoding is not a speed setting. It is a pair you
measure.

*Published 2026-08-06; withdrawn 2026-08-10 when three larger Gemma runs lacked
MTP-off partners; republished 2026-08-11 after those pairs completed. Rakuen
builds aimee, the system measured here. Every figure traces through the
[figure map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/speculative-decoding-was-free/evidence/figures.md).*

A draft model guesses several tokens. The target checks them together and keeps
the ones it would have produced itself. Gemma and Qwen call their native draft
heads multi-token prediction (MTP). Glimmer uses a diffusion drafter called
DFlash. Both are speculative decoding.

## Five complete pairs close the evidence gap

The withdrawn article had six small Gemma pairs and one Qwen pair. Its 12B, 26B
and 31B Gemma results had no matching MTP-off runs. They do now. So does
Qwen3.6-35B-A3B.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-pairs" id="fig-pairs-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-pairs" id="fig-pairs-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-pairs-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-pairs-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 226" preserveAspectRatio="xMidYMid meet" role="img" aria-label="MTP speedup for five matched model pairs"><line class="sg-chart__rule" x1="220" x2="220" y1="22" y2="180"/><text class="sg-chart__value" x="220" y="198" text-anchor="middle" opacity=".7">1x</text><line class="sg-chart__grid" x1="345" x2="345" y1="22" y2="180"/><text class="sg-chart__value" x="345" y="198" text-anchor="middle" opacity=".7">1.5x</text><line class="sg-chart__grid" x1="470" x2="470" y1="22" y2="180"/><text class="sg-chart__value" x="470" y="198" text-anchor="middle" opacity=".7">2x</text><line class="sg-chart__grid" x1="595" x2="595" y1="22" y2="180"/><text class="sg-chart__value" x="595" y="198" text-anchor="middle" opacity=".7">2.5x</text><text class="sg-chart__label" x="208" y="48" text-anchor="end">Gemma 4 12B</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="39.5" width="385" height="9" rx="4"/><text class="sg-chart__value" x="614" y="48">2.54x</text><text class="sg-chart__label" x="208" y="76" text-anchor="end">Gemma 4 26B-A4B</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="67.5" width="180" height="9" rx="4"/><text class="sg-chart__value" x="409" y="76">1.72x</text><text class="sg-chart__label" x="208" y="104" text-anchor="end">Gemma 4 31B</text><rect class="sg-chart__mark sg-chart__mark--1" x="220" y="95.5" width="264" height="9" rx="4"/><text class="sg-chart__value" x="493" y="104">2.05x</text><text class="sg-chart__label" x="208" y="132" text-anchor="end">Qwen3.6-27B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="123.5" width="338" height="9" rx="4"/><text class="sg-chart__value" x="567" y="132">2.35x</text><text class="sg-chart__label" x="208" y="160" text-anchor="end">Qwen3.6-35B-A3B</text><rect class="sg-chart__mark sg-chart__mark--2" x="220" y="151.5" width="163" height="9" rx="4"/><text class="sg-chart__value" x="392" y="160">1.65x</text><text class="sg-chart__axis" x="470" y="220" text-anchor="middle">THROUGHPUT WITH MTP DIVIDED BY THROUGHPUT WITHOUT IT</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">model</th><th style="text-align:right">MTP off</th><th style="text-align:right">MTP on</th><th style="text-align:right">faster</th><th style="text-align:right">F1 change</th><th style="text-align:right">kept</th></tr></thead><tbody><tr><td style="text-align:left">Gemma 4 12B</td><td style="text-align:right">96.33 tok/s</td><td style="text-align:right">244.73 tok/s</td><td style="text-align:right"><strong>2.54x</strong></td><td style="text-align:right">+0.0079</td><td style="text-align:right">80.39%</td></tr><tr><td style="text-align:left">Gemma 4 26B-A4B</td><td style="text-align:right">193.04 tok/s</td><td style="text-align:right">332.36 tok/s</td><td style="text-align:right"><strong>1.72x</strong></td><td style="text-align:right">−0.0029</td><td style="text-align:right">79.21%</td></tr><tr><td style="text-align:left">Gemma 4 31B</td><td style="text-align:right">33.54 tok/s</td><td style="text-align:right">68.93 tok/s</td><td style="text-align:right"><strong>2.05x</strong></td><td style="text-align:right">−0.0026</td><td style="text-align:right">79.09%</td></tr><tr><td style="text-align:left">Qwen3.6-27B</td><td style="text-align:right">34.82 tok/s</td><td style="text-align:right">81.78 tok/s</td><td style="text-align:right"><strong>2.35x</strong></td><td style="text-align:right">−0.0003</td><td style="text-align:right">79.04%</td></tr><tr><td style="text-align:left">Qwen3.6-35B-A3B</td><td style="text-align:right">112.97 tok/s</td><td style="text-align:right">186.78 tok/s</td><td style="text-align:right"><strong>1.65x</strong></td><td style="text-align:right">−0.0068</td><td style="text-align:right">76.63%</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">Five same-card pairs over the same 1,001 notes. Gemma used the same 4-bit quant on both sides; Qwen did the same. Every paired accuracy range crossed zero.</figcaption></figure>

F1 is the combined precision and recall score. A change of +0.0079 looks like a
small accuracy win. It is not one. Its 95% range runs from −0.0050 to +0.0209,
which includes no change. All five ranges include zero.

The six earlier 10,000-note Gemma pairs agree. Their paired changes ran from
−0.0021 to +0.0039, and every 95% range crossed zero, while throughput rose
1.84x to 2.31x. Across eleven pairs, the speed result is large. The accuracy
result is unresolved.

## Glimmer exposed a backend bug, not an MTP verdict

Muse Glimmer looked like the counterexample. Its official 17GB target ran at
41.39 tokens/s on the XTX. Adding Meta's matching DFlash drafter cut that to
37.67 tokens/s over the same first 22 notes.

<figure class="sg-figure"><input class="sg-figure__radio sg-figure__radio--chart" type="radio" name="fig-glimmer" id="fig-glimmer-chart" checked><input class="sg-figure__radio sg-figure__radio--table" type="radio" name="fig-glimmer" id="fig-glimmer-table"><div class="sg-figure__tabs"><label class="sg-figure__tab sg-figure__tab--chart" for="fig-glimmer-chart">Chart</label><label class="sg-figure__tab sg-figure__tab--table" for="fig-glimmer-table">Numbers</label></div><div class="sg-figure__panes"><div class="sg-figure__pane sg-figure__pane--chart"><svg class="sg-chart" viewBox="0 0 760 150" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Muse Glimmer generation speed with DFlash off and on"><text class="sg-chart__axis" x="0" y="24">MUSE GLIMMER 30B K-QUANT-17GB ON THE RX 7900 XTX</text><text class="sg-chart__label" x="180" y="61" text-anchor="end">DFlash off</text><rect class="sg-chart__mark sg-chart__mark--1" x="194" y="52.5" width="350" height="9" rx="4"/><text class="sg-chart__value" x="553" y="61">41.39 tok/s</text><text class="sg-chart__label" x="180" y="94" text-anchor="end">DFlash on</text><rect class="sg-chart__mark sg-chart__mark--2" x="194" y="85.5" width="319" height="9" rx="4"/><text class="sg-chart__value" x="522" y="94">37.67 tok/s</text><text class="sg-chart__axis" x="194" y="132">9% SLOWER · 24.5% OF DRAFT TOKENS KEPT</text></svg></div><div class="sg-figure__pane sg-figure__pane--table"><table><thead><tr><th style="text-align:left">same 22 notes</th><th style="text-align:right">DFlash off</th><th style="text-align:right">DFlash on</th></tr></thead><tbody><tr><td style="text-align:left">median generation</td><td style="text-align:right">41.39 tok/s</td><td style="text-align:right">37.67 tok/s</td></tr><tr><td style="text-align:left">aggregate throughput</td><td style="text-align:right">40.57 tok/s</td><td style="text-align:right">35.71 tok/s</td></tr><tr><td style="text-align:left">draft acceptance</td><td style="text-align:right">not applicable</td><td style="text-align:right">24.55%</td></tr></tbody></table></div></div><figcaption class="sg-figure__caption">The DFlash run was stopped after 22 matched notes. That is enough for the bounded speed and acceptance result, not an accuracy comparison.</figcaption></figure>

This was not warm-up. Acceptance was 28.3% over the first five notes and about
22% over the next five. The draft never approached the 77% to 80% band where
Gemma and Qwen won back its overhead.

The evidence points to the llama.cpp Vulkan path. Meta's
[August 2026 model card](https://huggingface.co/meta-models/Muse-Glimmer-30B-GGUF)
reports a 3.1x DFlash gain for this pair on an RTX 5090. llama.cpp has public reports of DFlash
slowing inference on [AMD hardware](https://github.com/ggml-org/llama.cpp/issues/25117)
and producing low acceptance under
[Vulkan](https://github.com/ggml-org/llama.cpp/issues/25792). We ran build b10356,
after Glimmer support landed in b10353; I found no relevant fix in the
[b10359 release notes](https://github.com/ggml-org/llama.cpp/releases/tag/b10359).

Calling this "MTP hurts Glimmer" would have been easy and wrong. DFlash is not
Glimmer's native MTP head, and a broken backend path says nothing general about
speculative decoding. It says the exact deployment failed its test.

## Score-stable does not mean identical

MTP should preserve the target model's choice. Batched checking can still change
floating-point arithmetic. In a deterministic 100-note Gemma check, MTP-off
reproduced 100 outputs; MTP-on reproduced 74.

Those text changes did not resolve into an F1 loss across the larger pairs.
Qwen showed the same score stability. We did not repeat the byte-for-byte check
on Qwen, so the 26 changed outputs belong to Gemma alone.

## Measure the pair, then decide

I first reported a 5.3x MTP gain by comparing a finished run with another run
still fighting fifteen orphaned clients. I then reported 1.58x by counting model
startup as generation. Both numbers were wrong.

The replacement is short:

- Run on and off with the same model, quant, card, notes and concurrency.
- Verify the loaded target, the draft and the server's accepted-token counters.
- Report throughput with a paired accuracy range.

Gemma and Qwen pass that test here. Glimmer on Vulkan does not. Enable
speculative decoding only after the pair wins on the machine that will run it.

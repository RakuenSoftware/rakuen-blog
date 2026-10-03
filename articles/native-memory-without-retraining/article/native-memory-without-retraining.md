---
title: "We Gave AI Models Memory Without Retraining Them"
slug: native-memory-without-retraining
date: 2026-10-01
author: Jared Bailes
tags: [aimee, native-memory, ai-memory]
excerpt: "Aimee lets AI models use shared, updateable knowledge directly. Our new paper measures what that changes for accuracy, context space and time."
---

We have published the [first paper on Aimee's native memory](https://zenodo.org/records/23077865). It reports the result we built Aimee to reach: a model can use knowledge it was never trained to know, without having that knowledge pasted into its conversation. In our controlled comparison, native memory answered the tested questions as accurately as putting the same selected facts in the prompt, while leaving the conversation room for other work.

*Rakuen builds aimee. The [reporting record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/native-memory-without-retraining/evidence/figures.md) maps the figures in this article to the preprint.*

The distinction matters because most AI systems give the model two jobs. It has to reason about a question, and it has to carry the facts needed to answer it. We built Aimee around a different division: reasoning belongs to the model; memory and the rules for using it belong to the system around the model.

## A fact should not need a new model

Consider a company policy that changes today. A model trained last month cannot have learned that change in its weights. Retraining is expensive and slow, so the usual answer is to search for the new policy and paste the relevant text into the model's prompt. That works: the model can read the policy and answer from it.

But every pasted document, note and correction takes part of the model's finite context window. That window also has to hold the user's request, earlier conversation, instructions, working files and the answer the model is about to write. If the conversation continues, retained memory text keeps occupying that window. If the system retrieves it again for a later request, it adds text again.

Aimee keeps the authoritative knowledge outside the model. When a question arrives, the memory system selects records the request is allowed to use. The selected knowledge reaches the model through its attention computation, the part that weighs information while forming an answer, rather than as text in the conversation. The trained weights stay fixed, and the memory can change independently of them.

That is what we mean by *native memory*. It is selected memory, not a hidden chat message or a change to trained weights. Yet a model can learn in the practical sense: a 12-billion-parameter model used validated procedures learned by a 27-billion-parameter model, raising its score from 165/480 to 276/480 on the same tasks. Knowledge transferred from the larger model; trained weights did not.

## Context space is a continuing cost

A token is a small piece of text that occupies a position in the model's input. A prompt has a limited number of those positions. Once thousands of positions are used to repeat background facts, the model has less room for the actual task. A longer conversation can force the system to drop older material, summarise it, or stop.

The cost continues after the first answer. If one memory passage stays in the conversation for ten requests, it occupies space on each of those ten requests. If each turn adds another passage and the earlier ones remain, the first request carries one, the second carries two, the third carries three. Across ten requests, that is 55 passage appearances.

The growth is quadratic across the conversation: for *n* turns, the total is *n(n + 1) / 2* passage appearances, even though only *n* distinct passages were added. This is an illustration of repeated context occupancy, not a measured bill.

Some services cache repeated prefixes, which can reduce computation or billing for that text. Caching does not give the context positions back. Each retained passage still competes with the instructions, documents and working history the model needs later.

In the paper's matched test, supplying 64 general-knowledge records as text occupied a median **4,580 prompt tokens**. Supplying those same selected records natively added **0 memory-text tokens** to the prompt. If one such passage remained for ten further requests, it would occupy 45,800 input-token positions across those requests.

If new passages accumulate as well, the repeated occupancy grows faster. These examples explain the cost curve; they are not extra test results.

Context saving does more than free space. A policy pasted for one question can linger after it changes or the discussion moves on, pulling a later answer toward an obsolete fact. Native memory leaves no memory text behind in the conversation: Aimee supplies selected, authorised knowledge for the current request without carrying that passage into the next prompt. That removes this source of context pollution along with its recurring token cost.

## The measured comparison kept accuracy while freeing context

The fair baseline is ordinary retrieval: select the same records, then give their text to the model. We compared that baseline with native memory using a fixed Gemma model. The [47,065-response study](https://zenodo.org/records/23077865) included 10,000 general-knowledge questions and 625 personal-knowledge questions. Native and text delivery each answered those questions correctly.

Both also answered every tested question with up to 64 selected records, including other records that might distract the model.

| With 64 selected general-knowledge records | Records as prompt text | Native memory |
| --- | ---: | ---: |
| Correct answers in the pressure test | 625/625 | 625/625 |
| Median prompt tokens added by memory text | 4,580 | 0 |
| Median time to first answer token | 2,565 ms | 156 ms |

*Source: [Shared Native Memory, Appendix E](https://zenodo.org/records/23077865). Timings use prepared memory in host RAM and measure this test setup, not every deployment.*

Across the entire matched campaign, the text condition added **7,366,848 memory-related prompt tokens** that the native condition did not add. Total prompt tokens in these requests fell from 8,026,911 to 660,063, a **91.78% reduction** for this workload. That is a count of input tokens, not a measured reduction in dollars. Preparing native memory uses compute and storage, and a provider's prices and caching rules decide what any customer actually pays.

The time result is specific to prepared memory. Other record counts and cold preparation have different costs, which the paper reports separately.

## The knowledge can outlive the model

The same separation changes how updates work. We tested corrections to stored facts while the models' trained weights stayed unchanged. We also measured retained improvements on repeated tasks. Aimee can carry what earlier work established into later work, including when that work uses another model.

The whole knowledge store need not sit in expensive GPU memory. In the system described by the paper, a local copy lives on disk, with an index and working cache in ordinary RAM. Only the selected native state needs space on the device. This does not make retrieval or preparation free, but adding knowledge no longer means putting every fact into every model's trained weights.

That is a different kind of capacity from adding parameters to a model. It increases the knowledge the system can make available to a model, but our tests do not assign a number of equivalent trained parameters. Nor do they show the model changing its underlying reasoning weights. Improving reasoning while a model runs is Aimee's next research goal; the results reported here establish shared knowledge consumption and retained experience.

The large accuracy comparison used controlled questions and selected facts. It does not measure unrestricted search across the knowledge base or open-ended reasoning over many facts. The production path still has to pay for selection, preparation, storage and access control. Those costs belong in an end-to-end comparison before anyone claims a universal dollar saving.

What we have established is the architectural boundary we set out to build: knowledge can be stored, corrected and shared outside a reasoning model, then consumed by that model without filling its conversation with the same facts. The [full preprint](https://zenodo.org/records/23077865) contains the methods, unsuccessful attempts, timing conditions and remaining work.

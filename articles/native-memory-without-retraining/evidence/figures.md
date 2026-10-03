# Source and figure record

This article reports no new tests. Its quantitative statements are a lay summary of Jared Bailes, *Shared Native Memory: Expanding Knowledge Without Retraining*, Zenodo preprint, October 1, 2026, DOI [10.5281/zenodo.23077865](https://zenodo.org/records/23077865). The paper contains the protocol, model configurations, raw-result references and limitations. This record maps each blog claim to the preprint and is not a replacement for its methods.

| Blog claim | Source in preprint | Scope |
| --- | --- | --- |
| Live corrections with fixed weights | Section III-B and Appendix B | Controlled corrections to external memory; the models' trained weights did not change. |
| Transfer from a 27B donor to a 12B receiver; 165/480 to 276/480 correct tasks | Abstract; Section III-C | Validated procedures from the larger model improved the smaller model on the same tested tasks, with fixed weights. This is not wholesale transfer of a larger model's knowledge or reasoning ability. |
| Retained task improvement | Abstract; Sections III-D and III-E; Appendix D | Fixed-weight, repeated-task learning demonstrations, not changed reasoning weights. |
| 47,065 responses; 10,000 general and 625 personal questions; accuracy parity with text | Abstract; Section III-E; Appendix E | Gemma matched text retrieval on controlled questions with selected records. This is not arbitrary-question accuracy. |
| Up to 64 selected records at 100% accuracy | Abstract; Section III-E; Appendix E | Matched native and text pressure comparisons on the tested single-fact fixtures. |
| Median 4,580 prompt tokens, 2,565 ms text versus 156 ms native | Abstract; Section III-E; Appendix E | 64 general records; prepared host-memory state; median time to first token. Other cohort and cold-path timings differ. |
| 7,366,848 memory-related tokens avoided; total prompt tokens 8,026,911 to 660,063, or 91.78% | Appendix E-B | Summed input tokens in the 47,065-response matched campaign, including repeated fixtures and pressure sizes; not a billing or end-to-end cost measurement. |
| Ten accumulated passages appear 55 times across ten requests | Illustrative arithmetic: 1 + 2 + ... + 10 = 55 | Assumes one new equal-size passage each turn, all prior passages retained, and a prompt containing the accumulated text on every request. This is not an experiment. |
| A 4,580-token passage occupies 45,800 input-token positions across ten later requests | Illustrative arithmetic: 4,580 × 10 = 45,800 | Assumes the passage remains in the prompt on all ten requests. This is not a measured bill. |
| Disk-backed local store, RAM index/cache, selected device state | Section II-B | Architectural storage tiers described in the paper; not a quantified cost saving. |
| Avoiding lingering memory-text context pollution | Sections II-A and II-B; Appendix E-B | Architectural consequence of native delivery without memory text in the conversation. The paper measured zero memory-text prompt tokens; it did not run a separate answer-contamination benchmark. |

The first draft's first-party results are all retained in the revised article: live corrections, 27B-to-12B transfer, repeated-task improvement, 47,065-response accuracy comparison, 64-record pressure accuracy, median context tokens and first-token timing. The revision adds the paper's aggregate prompt-token totals and clearly labelled arithmetic examples. No first-party result was removed.

Interest disclosure: Rakuen builds aimee. This article explains the company's own research. It makes no independent-replication claim.

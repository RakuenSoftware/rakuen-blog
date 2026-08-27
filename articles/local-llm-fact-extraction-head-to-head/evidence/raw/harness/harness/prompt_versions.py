"""Render an older prompt version from the live template, by explicit reversal.

A v5-vs-v7 comparison needs both prompts on the same corpus and the same server,
but prompt.py deliberately holds exactly one template -- the one production
sends -- and verifies it byte-for-byte against the C source. Keeping a second
copy of v5 here would defeat that check the moment either drifted.

So older versions are DERIVED from the live one by named substitutions, and each
substitution asserts it matched. If the live wording moves, this raises instead
of silently producing a prompt that is neither version.
"""

import prompt

# v6/v7 replaced these two spans. Both are reversed to recover v5.
SCHEMA_LIVE = ('{"facts":[{"subject":"","relation":"","object":"","confidence":0.0,'
               '"negated":false}]}')
SCHEMA_V5 = '{"facts":[{"subject":"","relation":"","object":"","confidence":0.0}]}'

RETRACT_LIVE_START = "emit the ORIGINAL fact it retracts"
RETRACT_LIVE_END = 'omit "negated" or set it false. '
RETRACT_V5 = ("do NOT emit the negated fact - a retraction asserts a fact is FALSE, "
              "so there is nothing durable to record. ")

# v7 added only this sentence on top of v6.
RENAME_V7 = ('A RENAME is NOT a retraction: "A is now called B" means A and B are '
             "the same thing, so emit also_known_as with negated FALSE. ")


def _require(hay, needle, what):
    if needle not in hay:
        raise SystemExit(f"prompt_versions: {what} no longer matches the live template.\n"
                         f"  looked for: {needle[:80]!r}")
    return hay


def live():
    prompt.verify_against_source()
    return prompt.system_prompt()


def v5(text=None):
    """The pre-polarity prompt: reasoning granted, retraction discarded."""
    s = text if text is not None else live()
    _require(s, SCHEMA_LIVE, "schema line")
    s = s.replace(SCHEMA_LIVE, SCHEMA_V5, 1)
    _require(s, RETRACT_LIVE_START, "retraction guidance")
    i = s.index(RETRACT_LIVE_START)
    j = s.index(RETRACT_LIVE_END, i) + len(RETRACT_LIVE_END)
    return s[:i] + RETRACT_V5 + s[j:]


def v6(text=None):
    """v7 minus the rename sentence."""
    s = text if text is not None else live()
    _require(s, RENAME_V7, "rename sentence")
    return s.replace(RENAME_V7, "", 1)


# Diagnostic variants for the reasoning question, added deliberately and named
# so no arm can inherit one by accident.
#
# THE QUESTION. Seven of fourteen models in the head-to-head emit no reasoning
# pass at all under the live prompt. That is either the model or the prompt, and
# the project has already been burned once by assuming the former: on gemma-4-E4B
# a single sentence, "No prose, no markdown.", suppressed reasoning across 10,000
# notes while every row recorded thinking:true, and restoring it was worth +0.116
# relation-agnostic recall. E2B, same family, never had the behaviour.
#
# WHAT THESE ARE FOR, and what they are NOT for. Both produce arms that answer
# "does this prompt suppress this model's reasoning channel". Neither produces a
# number comparable to the ranking table: a model scored under a different prompt
# is a different configuration, exactly as a different process count is. Every
# prediction row records its own prompt_version, so nothing banked is touched and
# nothing can be silently mixed.
FINAL_LIVE = ("Reason first if it helps; the answer that follows must be the JSON "
              "object only, no prose, no markdown.")
FINAL_V4 = "No prose, no markdown."


def v4clause(text=None):
    """POSITIVE CONTROL. Restores the wording that provably suppressed E4B.

    This variant must reproduce the known failure or the experiment is not
    measuring what it claims: run gemma-4-E4B under it and reasoning should
    collapse to ~0. If it does not, the variant is wrong, not the models.
    """
    s = text if text is not None else live()
    _require(s, FINAL_LIVE, "final output-format sentence")
    return s.replace(FINAL_LIVE, FINAL_V4, 1)


REASON_LIVE = "Reason first if it helps;"
REASON_FORCED = ("Reason first on every note, including the ones where the answer "
                 "looks immediate;")


def forcereason(text=None):
    """COUNTERFACTUAL. Removes the model's discretion over whether to reason.

    The live prompt says "if it helps", so a note answered without reasoning is a
    choice the model made. E4B at Q6 makes it on about 13% of notes and the same
    weights at Q4 and Q8 almost never do, which says the build decides rather than
    the note. What no observation can say is whether those notes were cheap to
    skip or expensive: the model picks which ones go silent, so "silent notes
    score well" is equally consistent with reasoning being unnecessary there and
    with the model skipping the notes it happens to already know.

    Forcing reasoning breaks that tie, because the same note is then answered both
    ways. Only the conditional clause changes; everything else, including the
    output-format sentence that suppressed reasoning under v4, is untouched.

    The wording is a confound and the design absorbs it: notes that reasoned under
    BOTH prompts are the control. If those move as much as the forced-silent ones,
    the effect is the sentence rather than the reasoning, and the comparison is
    dead.
    """
    s = text if text is not None else live()
    _require(s, REASON_LIVE, "conditional reasoning clause")
    return s.replace(REASON_LIVE, REASON_FORCED, 1)


REASON_INSISTENT = (
    "Before the JSON, write at least one sentence of reasoning about this note. "
    "Do this on every note without exception, including notes where the answer is "
    "obvious and notes where there is nothing to extract;")


def forcereason2(text=None):
    """THE ESCALATION. Asks harder than forcereason, to price the instruction.

    forcereason moved 67 of 134 silent notes and left the other 67 exactly as they
    were, which is either a sentence that was not firm enough or a decision the
    prompt does not reach. One wording cannot tell those apart, and the article
    drawn from that run says the decision sits below the level a sentence reaches
    — a claim a stronger sentence can falsify.

    So this one removes the escapes the previous wording left open. It names a
    minimum ("at least one sentence"), forbids the exemption the model might infer
    ("including notes where the answer is obvious"), and covers the empty case
    ("nothing to extract"), which matters because a note with no durable fact is
    the one place skipping reasoning looks most defensible.

    It replaces the whole conditional clause rather than layering, so the rendered
    prompt has one instruction about reasoning and not two competing ones.
    """
    s = text if text is not None else live()
    _require(s, REASON_LIVE, "conditional reasoning clause")
    return s.replace(REASON_LIVE, REASON_INSISTENT, 1)


def noclause(text=None):
    """THE TEST. Removes the output-format constraint entirely.

    A model that reasons here and not under the live prompt is being suppressed
    by the prompt. A model that reasons under neither is not a reasoning model in
    this harness, and its place in the ranking is a capability result rather than
    a configuration artefact.

    Parse rate is expected to fall: the clause is doing real work, and removing it
    brought back fenced ```json output on 14 of 20 notes when this was measured on
    E4B. That is why this is a diagnostic and not a candidate prompt.
    """
    s = text if text is not None else live()
    _require(s, FINAL_LIVE, "final output-format sentence")
    return s.replace(FINAL_LIVE, "", 1).rstrip() + "\n"


ADDED_V8 = ("customer_of", "subscription_tier", "owns_account", "purchased",
            "founded", "mentors", "runs_on")


def v7(text=None):
    """v8 minus the seven relations the ontology gained, so 17 names, not 24.

    The template is byte-identical between the two versions. What changed is the
    canonical relation list interpolated into it, which is why a version scheme
    tracking only template text would have called these two runs comparable.

    Derived by removing the seven added names from the live list rather than by
    keeping a copy of the old one, on the same principle as every other version
    here: if a name is later renamed in rel_types.c this raises instead of
    quietly rendering a prompt that is neither version.
    """
    if text is not None:
        raise SystemExit("v7 rebuilds the relation list, so it cannot layer on "
                         "another version's text")
    prompt.verify_against_source()
    live_names = prompt.seed_relations()
    missing = [r for r in ADDED_V8 if r not in live_names]
    if missing:
        raise SystemExit("prompt_versions: v8 relations absent from the live "
                         f"ontology, so v7 cannot be derived: {missing}")
    kept = [r for r in live_names if r not in ADDED_V8]
    if len(kept) != 17:
        raise SystemExit(f"prompt_versions: v7 needs 17 relations, derived {len(kept)}")
    return prompt.TEMPLATE % ", ".join(kept)


VERSIONS = {"v5": v5, "v6": v6, "v7": v7, "v4clause": v4clause,
            "noclause": noclause, "forcereason": forcereason,
            "forcereason2": forcereason2}


def render(version):
    """`version` may be any key in VERSIONS, or 'live' for the shipped prompt."""
    if version == "live":
        return live()
    if version not in VERSIONS:
        raise SystemExit(f"unknown version {version!r}; have live, {', '.join(VERSIONS)}")
    return VERSIONS[version]()


if __name__ == "__main__":
    import sys
    v = sys.argv[1] if len(sys.argv) > 1 else "live"
    s = render(v)
    print(f"--- {v} ({len(s.encode())} bytes) ---")
    print(s)

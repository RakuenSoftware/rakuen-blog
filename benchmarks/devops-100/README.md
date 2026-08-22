# DevOps-100

DevOps-100 is a proposed benchmark of 100 hands-on repository and systems
tasks. It measures whether an agent can inspect an unfamiliar environment,
change it safely, and leave it verifiably better. It is not a multiple-choice
DevOps quiz and it does not award points for naming the right command.

The task catalog is [`tasks.tsv`](tasks.tsv). Every row specifies the broken or
incomplete environment presented to the agent and the externally observable
condition used to grade the result. The catalog deliberately spreads 10 tasks
across each of 10 domains:

| Domain | What it covers |
| --- | --- |
| `linux` | processes, boot, packages, storage, scheduling, and performance |
| `network` | routing, DNS, TLS, proxies, firewalls, VPNs, and load balancing |
| `containers` | image builds, runtimes, registries, provenance, and Compose |
| `kubernetes` | workloads, policy, scheduling, upgrades, and cluster recovery |
| `iac-cloud` | Terraform/OpenTofu, Ansible, images, cloud APIs, and drift |
| `cicd` | build graphs, release engineering, promotion, and rollback |
| `observability` | metrics, logs, traces, alerting, SLOs, and incident response |
| `security` | identity, secrets, policy, hardening, detection, and response |
| `data` | databases, queues, replication, migrations, backup, and restore |
| `platform` | developer platforms, tenancy, GitOps, cost, and resilience |

## Task contract

Each task runs in a disposable isolated environment. A task package should
contain:

```text
tasks/<id>/
  prompt.md                 information visible to the agent
  environment/              VM, OCI, kind, or mock-control-plane definition
  seed/                     deterministic initial and fault state
  tests/public/             small preflight and contract test set
  tests/private/            authoritative postcondition and regression tests
  solution/                 maintainer-only reference patch and runbook
  task.json                 timeout, capabilities, versions, and rubric weights
```

The prose in `tasks.tsv` is the fixture specification. Implementations must pin
all images and packages by digest or snapshot. Cloud tasks use local API
emulators or recorded deterministic control planes unless a separate live-cloud
track is declared. No benchmark task may depend on the public Internet while
the agent is running.

## Runnable reference package

`DEVOPS-056` is implemented end to end as the reference package. It presents a
broken release build whose artifacts depend on wall-clock time and whose Make
rule rebuilds unconditionally. Its private grader independently checks clean
reproducibility, incremental behavior, dependency tracking, overridden output
paths, safe cleanup, semantic content, and the operator-facing contract.

Use the dependency-free harness to inspect and run it:

```sh
python3 benchmarks/devops-100/devops_bench.py validate
python3 benchmarks/devops-100/devops_bench.py list
python3 benchmarks/devops-100/devops_bench.py prepare DEVOPS-056 /tmp/devops-056-work
cd /tmp/devops-056-work
python3 .devops-bench/public/check.py
# Make the requested repair, then grade from the repository:
python3 /path/to/devops-100/devops_bench.py grade DEVOPS-056 "$PWD"
```

`prepare` refuses to overwrite any existing path. It copies the prompt, seed,
and public checks but never the private grader or maintainer solution. In a real
evaluation the grader must additionally run in a namespace the agent cannot
inspect or modify.

## Evaluation

The harness captures the initial state, gives the agent a shell and the task
prompt, then runs private checks after the agent exits. A reboot or service
restart is performed when persistence matters. The harness also repeats the
agent's intended convergence command when the task promises idempotence.

The default score for each task is 100 points:

- 55 points: required functional postconditions
- 15 points: regressions and preservation of unrelated state
- 10 points: persistence across restart, reboot, or reconciliation
- 10 points: security and least-privilege invariants
- 5 points: idempotence or safe retry behavior
- 5 points: required diagnosis, change record, or operator artifact

Not every task uses every dimension. Its unused points move to functional
postconditions in `task.json`. A destructive shortcut, disabled security
control, fabricated evidence, leaked secret, or test tampering is a zero even
if the service responds successfully. The grader runs outside the agent's
namespace and hashes all private tests before and after execution.

Report both macro-average and per-domain scores. Also report success rate by
operation (`diagnose`, `repair`, `build`, `migrate`, `respond`, `optimize`,
`recover`, `review`) and difficulty. Partial credit must come from independent
postconditions; graders must never infer quality from the agent's explanation.

## Difficulty and realism

- `foundation`: one subsystem and a bounded failure; not necessarily easy.
- `intermediate`: several files or signals and at least one misleading clue.
- `advanced`: interacting subsystems, production constraints, or staged work.
- `expert`: ambiguous symptoms and a narrow safe path under incident pressure.

Prompts should describe symptoms and business constraints. They should not name
the faulty line, exact command, or implementation. Seed data must include
plausible noise. Private checks should perturb incidental values such as ports,
resource names, addresses, and replica counts to reject memorized patches.

## Safety model

All destructive operations target synthetic data in an ephemeral namespace.
The harness blocks access to the host, user credentials, metadata endpoints,
and external networks. Tasks involving compromise, credential rotation, or
data loss use canary secrets and generated records. Recovery tasks retain an
out-of-band snapshot so evaluation cannot damage another run.

## Catalog validation

Run:

```sh
python3 benchmarks/devops-100/validate_catalog.py
```

The validator enforces the count, ID sequence, controlled vocabulary, balanced
domains, unique titles, required task fields, and a minimum spread of operation
types and environments.

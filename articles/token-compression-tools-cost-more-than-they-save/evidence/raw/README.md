# Raw reporting artifacts

Files in this directory are append-only evidence. Do not delete, overwrite,
truncate, reformat or replace them during article work.

If a result is invalid or incorrect, add an adjacent Markdown note whose first
line is `STATUS: INVALID`. Record why the artifact is invalid and identify the
superseding artifact. Keep the original file. Deletion requires a reason in the
reporting ledger and the user's explicit approval.

Each new artifact must have an adjacent note recording:

- collection date and time;
- command or collection method;
- software version or commit;
- fixture or input;
- environment facts that bear on the result;
- expected and actual outcome;
- whether the run was valid.

Do not put credentials, private customer data or material the repository is not
authorised to publish in this directory.

# Optional Bailian verification

Bailian CLI is a development and optional verification layer. It is not a required runtime dependency and must not force a second user authorization.

## Use cases

When `bl` is already available and authenticated, it may:

- parse a JD image with `bl omni` and compare extracted role terms with the host Agent's extraction;
- re-check ambiguous interview-question screenshots with `bl omni`;
- supplement public-web discovery with `bl search web` only when the WebSearch MCP is activated;
- review the evidence ledger and Markdown for missing anchors or unsupported high-priority claims with `bl text chat`.

Inspect `bl <command> --help` before calling it. Do not assume WebSearch is activated merely because the CLI is installed.

## Failure behavior

If Bailian is missing, unauthenticated, timed out, quota-limited, or its WebSearch MCP is inactive:

1. skip the optional check;
2. record `Bailian verification: not run` and the non-sensitive reason;
3. continue the core Museon and host-Agent workflow;
4. never ask the user to authorize Bailian unless the user explicitly requests the optional verification.

Do not send a real resume or unnecessary personal information to an optional model. Prefer redacted excerpts or the minimum relevant crop.

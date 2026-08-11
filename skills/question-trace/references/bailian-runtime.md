# Required Model Studio runtime

Aliyun Model Studio CLI is a required runtime dependency. Use `qwen3.5-omni-plus` for two load-bearing steps in every QuestionTrace run:

1. normalize the current JD and resume into structured evidence;
2. extract visible questions and stage details from every accessible interview-experience image in a live run.

Do not replace these calls with host-model vision, a dry run, or a statement that Model Studio was used during development.

## Command discovery and preflight

Use `bl.cmd` on Windows when PowerShell blocks `bl.ps1`; use `bl` on other systems. Inspect the installed command before calling it:

```text
bl.cmd --version
bl.cmd omni --help
bl.cmd config show
```

Never print, copy, or store an API key. `config show` is for non-sensitive status only. Most Model Studio commands require the user's locally configured Model Studio credential.

## Required JD and resume normalization

Send the minimum required pages or redacted text. Repeat `--image` for multiple pages. Request JSON and text-only output:

```text
bl.cmd omni --model qwen3.5-omni-plus --text-only --output json --system "You extract only visible facts. Do not invent missing experience, metrics, dates, employers, education, or skills." --message "Normalize the attached JD and resume into JSON with role, company, hiring type, seniority, business domain, responsibilities, must-have skills, preferred skills, candidate experiences, metrics, gaps, and likely interviewer triggers. Label observed and inferred fields separately." --image <jd-page> --image <resume-page>
```

For text-only inputs, pass redacted JD and resume text through `--message`; the Model Studio call remains required. Validate the returned JSON before using it to build queries.

## Required interview-image extraction

Use one source at a time and preserve image order. Prefer the smallest readable crop that contains the interview content:

```text
bl.cmd omni --model qwen3.5-omni-plus --text-only --output json --message "Read only visible text in this interview-experience image. Return JSON with image_index, visible_questions in original order, interview_stage, company, role, uncertain_text, and notes. Do not infer cropped or unreadable content." --image <temporary-image-or-authorized-url>
```

Validate that the output corresponds to the expected source and image index. Mark unclear characters instead of repairing them from model memory.

## Runtime audit record

Record only non-sensitive execution evidence:

- CLI version;
- model: `qwen3.5-omni-plus`;
- JD/resume normalization status;
- successful and failed call counts;
- processed image count;
- timestamp and output hash;
- `raw_media_retained: false`.

Do not store prompts containing contact details, raw resumes, original post bodies, expiring media URLs, or credentials in the repository.

## Failure behavior

If Model Studio CLI is missing, unauthenticated, timed out, quota-limited, or returns unusable output:

1. stop the evidence-backed workflow;
2. report the non-sensitive error and the failed stage;
3. ask the user to complete Model Studio setup or retry;
4. do not silently fall back to host-model OCR or vision;
5. do not label a replay or prior development run as the current required call.

WebSearch MCP is not required by QuestionTrace. Museon remains the discovery and source-reading layer; Model Studio remains the required multimodal evidence-extraction layer.

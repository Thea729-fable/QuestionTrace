---
name: question-trace
description: Generate an evidence-backed, personalized interview preparation question bank from a user's uploaded job description and resume. Use when a user asks for 面试押题、面经调研、面试题库、岗位面试准备、JD 与简历匹配、模拟面试，or wants fresh role-specific interview experiences retrieved through Museon CLI and normalized or visually extracted through Aliyun Model Studio CLI, with traceable sources, runtime audit, and Markdown output.
---

# QuestionTrace

Turn a JD, a resume, and fresh role-specific interview evidence into a traceable preparation-priority question bank for any role with accessible public interview evidence. Use Museon as the live discovery and source-reading layer. Use Aliyun Model Studio CLI with `qwen3.5-omni-plus` as a required runtime layer for JD/resume normalization and question-image extraction. Build a run-specific evidence ledger before predicting questions; do not substitute generic model recall or a prewritten role bank for retrieval. Treat every prediction as a preparation recommendation, never a guarantee of what an interviewer will ask.

## Required inputs

Require both:

- the target job description, as text, image, PDF, or document;
- the candidate resume, as text, image, PDF, or document.

Ask only for an input that is genuinely missing or unreadable. Do not ask the user to restate content that can be extracted from an uploaded file.

Protect personal data. Send only the minimum necessary input to Model Studio: prefer redacted pages or crops and exclude contact details when they are not needed for role analysis. Never include credentials in files or output. Never publish or commit a real resume without explicit approval. Do not invent missing experience, metrics, employers, dates, skills, or education.

## Load references by stage

Read these files before the corresponding stage:

- Read [references/bailian-runtime.md](references/bailian-runtime.md) before parsing any JD/resume input or analyzing any question image.
- Read [references/jd-resume-mapping.md](references/jd-resume-mapping.md) before generating search terms or building the three-way map.
- Read [references/museon-runtime.md](references/museon-runtime.md) before any Museon command, authentication recovery, Xiaohongshu search, or Nowcoder discovery.
- Read [references/research-protocol.md](references/research-protocol.md) before selecting or opening interview experiences and images.
- Read [references/evidence-model.md](references/evidence-model.md) before deduplication, frequency counting, evidence grading, or question scoring.
- Read [references/output-spec.md](references/output-spec.md) before writing the final Markdown.

Use [assets/question-bank-template.md](assets/question-bank-template.md) for the deliverable and [assets/evidence-ledger-template.json](assets/evidence-ledger-template.json) for the research ledger.

## Choose a run mode

Use **live research mode** by default. Run the required Model Studio input-normalization step, retrieve fresh evidence for the inferred role through Museon, and use Model Studio for every readable question image.

Use **evidence replay mode** only when the user supplies an existing evidence set, Museon is unavailable after recovery, or a demo explicitly requests replay. Still run the required Model Studio input-normalization step for the current JD and resume. Label replay output with the evidence collection date and the historical image-processing tool. Never describe replay evidence as a current live search or as a new Model Studio image-analysis run.

Model Studio is required in every mode. If `bl`/`bl.cmd` is missing, unauthenticated, quota-limited, or the required call fails, stop before generating an evidence-backed bank. Report the non-sensitive failure and ask the user to configure Model Studio; do not silently replace it with host-model vision or generic recall.

If live research is unavailable, offer one of these non-deceptive fallbacks:

1. resume-and-JD-only provisional preparation plan, clearly labeled as lacking live interview evidence;
2. evidence replay using a supplied or bundled demonstration set;
3. resume live research after Museon authorization or service recovery.

## Workflow

### 0. Verify the required runtimes

Inspect Model Studio CLI and Museon CLI versions and schemas without exposing credentials. Complete the required Model Studio input-normalization call before research. In live mode, recover Museon authentication only after a read command returns an authentication error.

### 1. Parse the JD and resume through Model Studio

Use `qwen3.5-omni-plus` through Model Studio CLI to normalize the JD and resume into structured facts. This call is mandatory even when the inputs are text-only. Extract the canonical role, role variants, company if present, business domain, seniority, responsibilities, must-have skills, preferred skills, collaboration expectations, metrics, and likely interview stages.

Extract each resume experience, claimed result, method, tool, ownership boundary, collaboration relationship, metric, chronology, and possible credibility gap. Separate facts from interpretation. Build a JD-to-resume mapping before researching interview experiences.

### 2. Build a role-specific query ladder

Derive queries from the uploaded JD. Never use a fixed role such as AI product manager when the JD describes another job.

Generate the ladder in this order:

1. exact company + exact role + 面经/面试;
2. exact role + 校招/实习/社招 + 面经;
3. role aliases and adjacent titles evidenced by the JD;
4. business domain + role, such as 商业化产品经理、广告产品经理、变现产品经理;
5. critical capability + interview, only when exact-role evidence is sparse.

Show the final query set in the research notes. Do not silently broaden into unrelated jobs.

### 3. Retrieve candidates from Xiaohongshu and Nowcoder

Use Xiaohongshu and Nowcoder as primary sources:

- Search Xiaohongshu natively through Museon.
- Discover Nowcoder pages through Museon public web research, using queries such as `site:nowcoder.com <role> 面经`, then open each candidate URL.
- Supplement with other public sources only when they improve exact-role coverage or recency. Label every platform.

Search for both relevance and recency. Use the last three years as the default eligibility window and weight the newest six months most strongly. Adapt the window only when the user requests another range or the role is too new to have older evidence.

### 4. Screen candidates without counting them

Treat search result titles and snippets only as discovery leads. A candidate does not enter the evidence set, frequency denominator, or source count until it passes the deep-reading gate.

Exclude obvious ads, generic coaching posts without first-hand questions, duplicates, reposts, inaccessible pages, and experiences unrelated to the inferred role. Record the exclusion reason.

### 5. Deep-read every selected experience

For every source included in analysis:

1. open the original page or post;
2. read the complete available body, not only the search snippet;
3. identify company, role, date, interview stage, candidate context, and all stated questions;
4. enumerate every attached image or carousel slide;
5. send every accessible image to `qwen3.5-omni-plus` through Model Studio CLI, batching only when the tool imposes a limit;
6. transcribe visible questions faithfully and mark uncertain characters;
7. record body completeness, total media count, Model Studio processed count, unreadable media count, model name, call status, and reason;
8. retain the source URL beside the extracted evidence.

Do not count a source as deeply read when its body is truncated and the remainder cannot be opened. Do not claim an inaccessible image or a failed Model Studio call was analyzed. Exclude incomplete sources from frequency claims unless the specific evidence used is independently visible and the limitation is explicit. Museon visual analysis may not substitute for the required Model Studio image step in a new live run.

Continue discovery until the planned query ladder is covered and two consecutive result pages or query variants add no new eligible source, or until a user-specified limit is reached. Report the actual stopping condition and sample size.

### 6. Build and validate the evidence ledger

Normalize one ledger record per original experience. Deduplicate the same author/post, mirrored URLs, copied question lists, and obvious reposts before counting frequency.

Run `scripts/audit_evidence.py <ledger.json>` when Python is available. The audit must verify the required Model Studio runtime record and, in live mode, Model Studio status for every accessible image. Fix all blocking errors before using the ledger for scoring. If Python is unavailable, apply the same checks manually and say so in the method note.

### 7. Extract themes and interviewer intent

Cluster semantically equivalent questions without erasing meaningful distinctions. For each cluster, identify:

- the underlying idea or capability;
- what the interviewer is trying to verify;
- strong-candidate qualities;
- common follow-up branches;
- observed company, role, and interview-stage context.

Keep observed questions separate from model-generated follow-ups. Label generated follow-ups explicitly.

### 8. Map evidence to the JD and resume

Require three anchors for every high-priority predicted question:

- interview-experience anchor: one or more deeply read sources;
- JD anchor: a quoted or accurately paraphrased requirement;
- resume anchor: the exact experience, skill, claim, or gap likely to trigger the question.

If one anchor is absent, reduce the priority or move the item to an exploratory section. Never make an unsupported question high priority.

### 9. Score preparation priority

Score each question cluster on a 15-point scale:

- source frequency: 0–4;
- recency: 0–3;
- JD relevance: 0–3;
- resume trigger strength: 0–3;
- company/role similarity: 0–2.

Use 12–15 for high priority, 8–11 for medium priority, and 0–7 for low priority. Call this **preparation priority**, not probability or hit rate. Use `scripts/score_priority.py` when a machine-readable score file is available.

### 10. Estimate interview duration and question count

Infer likely stages from the JD level, hiring type, role family, and observed evidence. State assumptions. Estimate time using main-question response length, follow-up depth, interviewer transitions, and candidate questions.

Use the duration to choose a realistic number of main questions. Distinguish the full preparation bank from one plausible interview route.

### 11. Generate the Markdown deliverable

Follow [references/output-spec.md](references/output-spec.md). Include:

- an answer-first prediction summary;
- JD and candidate fit analysis;
- research coverage and deep-reading audit;
- Model Studio runtime audit: CLI version, model, JD/resume status, image-call count, and failures;
- estimated process, duration, and question count;
- high-, medium-, and low-priority questions;
- resume deep dives, role skills, domain/business questions, behavioral questions, and candidate questions;
- interviewer intent, answer framework, follow-ups, and three anchors for each high-priority item;
- a timed mock-interview route;
- source ledger, exclusions, uncertainty, and limitations.

Save a Markdown file with a descriptive name such as `QuestionTrace_<company-or-domain>_<role>_<candidate>.md`. Return the absolute path and a concise summary.

## Third-party content boundary

- Access only content the user and the configured services are authorized to access.
- Do not bypass login walls, CAPTCHAs, robots restrictions, rate limits, or platform access controls.
- Treat search results as research leads, not as a license to redistribute platform content.
- Do not commit or redistribute original post bodies, creator identifiers, expiring media URLs, or question images.
- Retain only stable source links, minimal factual metadata, derived question text, hashes, and audit statuses needed for the user's preparation task.
- Process media transiently and record `raw_media_retained: false`.
- If a source cannot be read within these boundaries, mark it blocked and exclude it from unqualified frequency claims.

## Non-negotiable quality gates

- Do not say “all internet interview experiences” unless the research truly proves exhaustive coverage; state the searched platforms, window, queries, and sample count instead.
- Do not use a title, snippet, or search-card summary as if the full interview experience was read.
- Do not count any selected source until its body and all relevant images have explicit reading status.
- Do not fabricate inaccessible content, resume facts, citations, frequency, dates, or company context.
- Do not expose Museon, Bailian, browser, or service credentials.
- Require a successful `qwen3.5-omni-plus` Model Studio call in the core workflow; do not claim Model Studio participation from documentation or dry-run output alone.
- Do not describe Museon or Model Studio access as granting commercial rights to third-party platform content.
- Do not publish, schedule, or mutate any social account; this Skill performs read-only research and local document generation.

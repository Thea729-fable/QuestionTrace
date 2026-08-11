# Markdown output specification

Use an answer-first structure. Replace placeholders with actual evidence; do not leave template instructions in the final file.

## Required sections

1. **Prediction summary**
   - canonical role and company if known;
   - top capability themes;
   - estimated interview stages and duration;
   - plausible route question count;
   - explicit statement that scores are preparation priorities, not hit probabilities.

2. **JD and candidate analysis**
   - role model;
   - must-have and preferred capabilities;
   - resume strengths, gaps, credibility checks, and likely interviewer interest;
   - observed versus inferred labels.

3. **Research coverage and audit**
   - collection date and mode: live or replay;
   - platforms, time window, exact query families, and stopping condition;
   - candidates found, selected, deeply read, included, excluded, and blocked;
   - body-complete count;
   - image totals: found, read, not relevant, unreadable;
   - deduplicated source count;
   - Model Studio runtime: CLI version, model, JD/resume normalization status, successful/failed call counts, and live interview-image processed count;
   - data handling: raw interview media retained or discarded;
   - audit result: PASS or FAIL with exceptions.

4. **Priority question bank**
   - high, medium, and low preparation priority;
   - resume-experience deep dives;
   - role skill and domain questions;
   - business/company questions when evidence exists;
   - behavioral, collaboration, and pressure follow-ups;
   - questions the candidate can ask the interviewer.

5. **Timed mock route**
   - one plausible interview session, not the entire bank;
   - main-question count, follow-up branches, response-time guidance, and total duration.

6. **Evidence and limitations**
   - source ledger with original links;
   - excluded/blocked list with reasons;
   - unreadable-image disclosure;
   - sample and platform limitations;
   - generated-follow-up label.
   - third-party-content boundary: research links and minimal derived evidence only; no redistribution of raw post bodies, creator identifiers, expiring media URLs, or question images.

## High-priority question block

Every high-priority item must contain:

```markdown
### Qn. <question>

- Preparation priority: <score>/15 — High
- Score: frequency <x>/4 · recency <x>/3 · JD <x>/3 · resume <x>/3 · company/role <x>/2
- Interviewer intent: <what is being verified>
- Strong-candidate signal: <qualities demonstrated>
- Interview evidence:
  - [source label](original URL) — date, company, role, stage, body/image locator
- JD anchor: <quoted or faithfully paraphrased requirement>
- Resume trigger: <exact entry, claim, skill, or gap>
- Answer framework: <structure, not fabricated content>
- Likely follow-ups:
  1. <observed follow-up or clearly labeled generated follow-up>
- Suggested answer time: <minutes>
```

Medium and low items may be shorter, but must still distinguish observed evidence from generated preparation prompts.

## Citation rules

- Keep each original URL next to the claim it supports.
- Do not cite search-result URLs when an original post URL exists.
- Do not cite a source as fully read when the ledger says blocked, truncated, or unresolved.
- Do not expose local credential files or temporary signed URLs when a stable public source link exists.
- Do not reproduce full third-party posts or images in the final Markdown. Keep only the minimum question abstraction, locator, stable link, and audit metadata needed for preparation.
- In replay mode, disclose the historical image-processing tool exactly as recorded. Never relabel a Museon-processed replay as a new Model Studio run.

## Language and naming

Match the user's requested language; default to Chinese when the JD and resume are Chinese. Use `准备优先级`, never `命中概率`, `命中率`, or a fabricated percentage.

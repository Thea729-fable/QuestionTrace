# Evidence and scoring model

## Source unit

Count one original interview experience as one source unit. Multiple questions or images in the same post do not create additional source units. Deduplicated mirrors do not increase frequency.

## Evidence locator

Give every observed question a locator:

- body paragraph or section;
- image/slide number;
- interview stage if known;
- source ID and original URL.

Generated follow-ups must use a `generated_follow_up` label and may not be counted as observed frequency.

## Semantic clustering

Merge wording variants only when they test the same construct. Preserve distinctions that change the expected reasoning, such as product design versus metric diagnosis, or model evaluation versus model selection.

For each cluster retain:

- canonical question wording;
- observed wording variants;
- unique source count;
- newest and oldest supporting date;
- source/company/role distribution;
- image-backed versus body-backed count;
- interviewer intent and candidate quality signals.

## Fifteen-point preparation score

### Source frequency: 0–4

- 0: no deeply read source; cannot be high priority;
- 1: one unique source;
- 2: two unique sources;
- 3: three to four unique sources;
- 4: five or more unique sources or a strong cross-company pattern.

### Recency: 0–3

- 0: undated or older than three years;
- 1: within three years;
- 2: within one year;
- 3: within six months.

Use the newest strong supporting evidence, but do not hide an otherwise old sample distribution.

### JD relevance: 0–3

- 0: unrelated;
- 1: adjacent or generic;
- 2: clearly related to one responsibility or preferred skill;
- 3: directly tests a core responsibility or must-have skill.

### Resume trigger strength: 0–3

- 0: no candidate-specific trigger;
- 1: generic background relevance;
- 2: a clear skill, project, claim, or gap invites the question;
- 3: a prominent achievement, ownership claim, inconsistency, or role-critical experience strongly invites it.

### Company/role similarity: 0–2

- 0: only broad role-family evidence;
- 1: same role or same business domain;
- 2: same company and role, or a very close equivalent supported by the JD.

## Priority bands

- 12–15: high preparation priority;
- 8–11: medium preparation priority;
- 0–7: low preparation priority.

Never convert this score into a percentage or claim it is a calibrated hit probability.

## Guardrails

- A cluster with frequency score 0 cannot be high priority.
- A cluster missing any of interview, JD, or resume anchors cannot be high priority.
- A source with incomplete body or unresolved relevant images cannot support an unqualified frequency claim.
- A platform with many reposts must be deduplicated before comparison with another platform.

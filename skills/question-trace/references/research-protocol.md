# Deep research protocol

## Evidence states

Assign every discovered source exactly one state:

- `candidate`: found in search but not yet opened;
- `selected`: relevant and scheduled for deep reading;
- `included`: complete enough to support analysis;
- `excluded`: rejected with a reason;
- `blocked`: original content could not be fully accessed.

Only `included` sources contribute to sample count, frequency, recency distribution, or priority scoring.

## Deep-reading gate

A source may become `included` only when all applicable checks pass:

1. original URL or canonical post ID is present;
2. role relevance is verified from the original content;
3. full available body has been read;
4. interview date or publication date is recorded when available;
5. interview stage is extracted or marked unknown;
6. total attached media is counted;
7. every relevant image has status `read`, `not relevant`, or `unreadable with reason`;
8. all observed questions have a body or image evidence locator;
9. duplicate/repost status is resolved.

Do not interpret `0 images found` as `all images read` unless the original page genuinely has no media.

## Image procedure

For every selected carousel or screenshot set:

1. preserve original order;
2. inspect every image, not only the cover;
3. transcribe questions rather than summarizing them away;
4. retain page/image index for each extracted question;
5. distinguish visible text from interpretation;
6. mark blur, cropping, occlusion, or uncertain characters;
7. never reconstruct text outside the visible region.

When the tool accepts 12 media items per call, process images 1–12, 13–24, and so on. Reconcile the processed count with the source media count before inclusion.

## Completeness and stopping

Cover the full planned query ladder. Continue paginating or varying the controlled query until two consecutive pages or query variants add no new eligible original experience, or a user-set time/source cap is reached.

Report:

- platforms searched;
- exact query families;
- date window;
- candidates found;
- deeply read and included sources;
- blocked and excluded sources;
- total images found, read, irrelevant, and unreadable;
- stopping condition.

Do not describe bounded research as exhaustive of the internet.

## Deduplication

Group possible duplicates by:

- canonical URL or post ID;
- same author and materially identical body;
- same sequence of unusual questions;
- mirrored image sets;
- explicit repost attribution.

Keep the clearest original as the counting unit. Preserve duplicate URLs in its audit note but do not increment frequency.

## Observation versus inference

Use these labels consistently:

- `Observed`: directly visible in source, JD, or resume;
- `Interpreted`: semantic grouping or interviewer-intent analysis;
- `Inferred`: likely implication, stage, or follow-up;
- `Unknown`: not supported or not readable.

Keep source links adjacent to load-bearing observed claims.

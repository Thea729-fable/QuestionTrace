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
7. every relevant image has status `read`, `not relevant`, or `unreadable with reason`; in a live run, every accessible image also records a successful `qwen3.5-omni-plus` call;
8. all observed questions have a body or image evidence locator;
9. duplicate/repost status is resolved.

Do not interpret `0 images found` as `all images read` unless the original page genuinely has no media.

## Image procedure

For every selected carousel or screenshot set:

1. preserve original order;
2. inspect every accessible image through Model Studio `qwen3.5-omni-plus`, not only the cover;
3. transcribe questions rather than summarizing them away;
4. retain page/image index for each extracted question;
5. distinguish visible text from interpretation;
6. mark blur, cropping, occlusion, or uncertain characters;
7. never reconstruct text outside the visible region;
8. record the model, call status, timestamp, output hash, and `raw_media_retained: false`;
9. delete or discard temporary media after the run and never commit it to the repository.

Process one source at a time and preserve the image-to-source mapping. Reconcile the Model Studio processed count with the source media count before inclusion. Museon visual analysis cannot satisfy this gate for a new live run.

For evidence replay, preserve the historical image-processing tool and collection date. Do not relabel prior Museon or manual image analysis as a current Model Studio call. The current JD/resume normalization must still run through Model Studio.

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

## Data minimization

- Keep only stable original source links and the minimum metadata needed for audit.
- Do not retain creator identifiers unless essential and already public; redact them from demos by default.
- Do not store original post bodies, expiring CDN links, or copied question images in the repository.
- Store derived question text, source/image index, hashes, read status, and uncertainty instead.
- Treat blocked access as a stopping condition, not as permission to use another access route.

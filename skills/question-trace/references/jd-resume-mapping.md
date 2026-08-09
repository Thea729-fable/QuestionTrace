# JD and resume mapping

## 1. Build the role model

Extract only what the JD supports:

| Field | What to capture |
| --- | --- |
| Canonical role | Exact job family and specialization |
| Company | Named company or `not provided` |
| Hiring type | Internship, campus, experienced, unknown |
| Seniority | Entry, mid, senior, lead, unknown |
| Business domain | Product area, customer, monetization model |
| Core outcomes | What the role must deliver |
| Must-have capabilities | Explicit requirements |
| Preferred capabilities | Preferred or bonus requirements |
| Collaboration | Functions and influence expectations |
| Metrics | Growth, revenue, quality, efficiency, safety, etc. |

Do not reduce a specialized title to a generic title too early. For example, keep 商业化产品经理 as the canonical role and use 广告产品经理、变现产品经理 only as controlled expansions.

## 2. Build the candidate model

For each resume entry capture:

- situation and objective;
- claimed ownership;
- actions and methods;
- collaborators and decision boundaries;
- tools, models, data, or domain knowledge;
- result and metric;
- missing baseline, attribution, sample, or verification detail;
- relevance to each JD requirement;
- likely interviewer interest and credibility risk.

Never rewrite an inference as a resume fact. Use labels such as `observed`, `inferred`, and `missing`.

## 3. Build the query ladder

Generate queries from the role model:

1. `<company> <canonical role> 面经`
2. `<company> <canonical role> 一面/二面/终面`
3. `<canonical role> 校招/实习/社招 面经`
4. `<validated role alias> 面经`
5. `<business domain> <job family> 面经`
6. `<critical capability> <job family> 面试题`

Use the company only when the JD supplies it or the user confirms it. Keep an audit table showing which query produced which selected source.

## 4. Create the three-way map

For each predicted question record:

| Anchor | Required content |
| --- | --- |
| Interview evidence | Source IDs and observed question/theme |
| JD evidence | Exact bullet or faithful paraphrase |
| Resume trigger | Exact entry, claim, skill, gap, or chronology |

High priority requires all three. Medium priority may lack one strong anchor. Low priority may be a plausible exploratory topic, but must be labeled as such.

## 5. Estimate stages and time

Infer stages from observed same-role evidence and hiring type. Prefer the median observed structure when samples are sufficient. Otherwise use a conservative role-family estimate and state the assumption.

Estimate each route with:

`total = introductions + main answers + follow-ups + transitions + candidate questions`

Separate the complete preparation bank from a likely single-session route. Do not fit every bank question into one interview.

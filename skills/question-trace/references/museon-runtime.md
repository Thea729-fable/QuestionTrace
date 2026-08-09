# Museon runtime

## Command discovery

Treat the installed schema as the source of truth. Before first use in a run, inspect:

```text
museoncli schema research.social-media-search
museoncli schema research.web-research
museoncli schema research.visual-analyze
```

Do not invent flags. Parse JSON success and error responses.

## Authentication recovery

Do not run unconditional authentication checks. Start recovery only when a research command returns `missing_auth`, `unauthorized`, or a missing-workspace error.

1. Run `museoncli auth start`.
2. Show `verification_uri_complete` exactly as returned; never show the device code or credentials.
3. Run `museoncli auth finish --wait` in the same environment.
4. If several workspaces are plausible, list them and ask the user which one to select.
5. Resume the original research command after recovery.

## Xiaohongshu discovery and deep reading

Use the exact current schema. The expected stable flow in Museon CLI v0.5.9 is:

```text
museoncli research +social-media-search --platform xhs --intent keyword-search --query "<role query>" --limit 30 --content-chars 4000 --sort latest --time-window year --content-type image
```

Repeat with relevance sorting and controlled query variants. Follow returned pagination cursors when more results are needed.

Open every selected source using its returned post URL or ID:

```text
museoncli research +social-media-search --platform xhs --intent post --query "<post URL or ID>" --content-chars 4000
```

Search cards are discovery only. Record a source as body-complete only after the post call returns the full available body without an unresolved truncation warning.

Analyze every relevant image URL. The current visual command accepts at most 12 media items per call, so batch larger carousels while preserving image order:

```text
museoncli research +visual-analyze --media <image-url> --prompt "Transcribe every interview question and stage detail visible in this image. Preserve order, mark uncertain text, and do not infer missing content."
```

When signed media cannot be prepared, follow the returned media-import guidance. If an image remains inaccessible, mark it unreadable and do not claim it was analyzed.

## Nowcoder discovery and deep reading

Museon has no dedicated Nowcoder platform contract. Discover candidate pages with public web research:

```text
museoncli research +web-research --query "site:nowcoder.com <canonical role> 面经" --include search-results --limit 30 --content-chars 4000
```

Open each selected URL:

```text
museoncli research +web-research --url "<nowcoder URL>" --include page-text --content-chars 4000
```

If the returned page text is truncated, login-gated, or missing paginated content, use an available host browser/web reader to continue from the same original URL. If the complete body still cannot be read, exclude the source from deep-read frequency counts and record the reason.

## Other sources

Use Museon web research for additional public pages only after Xiaohongshu and Nowcoder coverage is established. Label platform, source type, and access quality. Do not substitute generic search snippets for original pages.

## Risk and privacy

These research commands are read-only under the inspected schema. Do not use publishing, scheduling, account mutation, or content-generation commands. Never log or expose authentication material, workspace tokens, resume contents beyond the user-requested output, or raw customer payloads.

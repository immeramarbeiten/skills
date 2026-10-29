# Saving earnings reports

The report must be usable after the chat ends. Explain where the full analysis and its chart are stored; a chat response or a lone chart does not constitute a saved report.

## Preferred destination: Google Drive

For users who want reports accessible on laptop and phone, use a native Google Doc in their connected Google Drive as the default when the user has requested or configured Drive saving. Use an existing user-owned report folder when configured; otherwise follow the connected Google Docs workflow’s default destination. If the user requests a dedicated `Earnings Desk` folder, create or reuse it in their own Drive. Follow the available Google Drive and Google Docs workflows for native-document creation and verify the finished file by readback. Avoid adding sharing permissions, and check folder access before writing to a shared destination. Give the user the actual Doc link.

Save the complete report, not only the opening wire: fiscal period, release and observation timestamps, all requested sections, clickable sources, measurement/basis caveats, and a descriptive chart caption. Embed a PNG chart when the available Docs workflow supports it; otherwise place the chart beside the report in the same folder and link it, retaining SVG when useful. Prefer a viewable PNG for mobile; do not promise an upload, embedding or file format unsupported by the connected tools. Give useful names such as `Alphabet GOOGL — Q3 FY2026 — 2026-10-28`.

## Document design

Treat the Google Doc as a crafted analyst research report, drawing on the clarity and information hierarchy of institutional research sheets while allowing a contemporary, original Earnings Desk style. Use a compact title and publication details, a prominent one-sentence thesis, the scannable wire, clear section hierarchy, concise tables where they improve comparison, callouts for pivotal evidence, and a source and limitations section. Keep interpretation clearly distinct from reported facts and quoted management statements. Avoid copying any firm's branding or proprietary layouts.

Use the document's supported features—headings, formatted text, tables, hyperlinks, embedded figures and captions—to make it navigable and readable. For a compact chart and related commentary, use a properly sized two-column table or another supported layout with the plot on the left and meaningful context on the right; remove distracting table borders and check the result. Stack or separate material if it becomes too small on a phone. Preserve the complete analysis and source links; verify imported content and embedded figures, and inspect a rendered preview when available. Google Docs is a static document destination: do not promise that chat interactions, live charts, or interactive widgets will survive conversion. Provide links or separate artifacts for such features when they are actually available.

## Alternative: private Git repository

If the user explicitly selects Git, identify the requested or configured repository and verify that it is private and writable before saving. Commit a readable Markdown report with source links and a relative path to SVG/PNG, using an organized company/period path. Respect the existing branch workflow and concurrent changes. Never store reports in a public skill repository merely because it holds the skill code. A public repository is suitable for the reusable skill itself when the user asks to update it.

## Unavailable destination

If the chosen connector, destination, or write action is unavailable, save the complete report and chart in the current workspace's user-facing output directory where available. Give the local links and explicitly state that the remote save did not happen. Do not claim success without checking the created file. Ask for a destination only when one cannot be inferred safely; do not repeatedly ask once a destination is configured.

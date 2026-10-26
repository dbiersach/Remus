# CLAUDE.md - Remus

Claude Code does not read `AGENTS.md` natively, so this file imports it. The line below
pulls in the full project rules and style guide.

@AGENTS.md

Keep all project, style, and formatting rules in `AGENTS.md` so that every AI tool used
with this repository follows the same guide. Add rules here only if they are specific
to Claude Code and meaningless to other tools.

## Chat responses

Responses are read in the Claude Code panel inside VS Code, which has no MathJax or
KaTeX renderer, so LaTeX shows up as literal dollar signs and backslashes.

- Write math as plain text: `2^n`, `<=`, `sqrt(2)`. Do not use `$...$` or `$$...$$`.
- Chat replies follow the repository's American spelling and no-long-dash rules.
- Use plain paragraphs for standard explanations rather than scattered bullets or bold.

## Git commits

Commit messages must carry no trace of AI assistance. Write the message as the
repository owner would have written it.

- Do not add a `Co-Authored-By: Claude ...` trailer, or any similar
  "co-authored by Claude" line.
- Do not add a generated-by footer such as "Generated with Claude Code" or a robot
  emoji tag.
- Do not credit the work in the subject or body either: no "with Claude's help",
  "AI-assisted", "per Claude's suggestion", or equivalent.
- Do not use vague verbs like "Refactor...", "Optimize...", or "Enhance..." unless
  followed by granular specifics. Never write passive commit messages.

The ban is on **attribution**, not on the words themselves. When a change is genuinely
*about* Claude or AI tooling, name it plainly:

- Good: `Add anthropic.claude-code to the extension install scripts`
- Good: `Document the chat math convention in CLAUDE.md`
- Bad: `Update install scripts (generated with Claude Code)`

# Skills

A collection of reusable agent skills for everyday workflows. Each skill lives in its own folder under `skills/` and contains a `SKILL.md` describing when and how to use it.

## Skills index

- [Earnings Desk](skills/earnings-desk/) — research public-company earnings, assess financial performance, and create an evidence-led report and infographic.

## Repository layout

```text
skills/
└── skill-name/
    ├── SKILL.md
    ├── references/   # Optional: supporting guidance
    ├── scripts/      # Optional: reusable helpers
    └── assets/       # Optional: templates or other assets
```

Only add supporting folders when a skill needs them. Each `SKILL.md` begins with YAML frontmatter containing a `name` and `description`.

## Using a skill in Codex

Ask Codex to install the desired skill from this repository, specifying its GitHub URL and path (for example, `skills/skill-name`). Review the skill and any scripts before installing or running them. Restart Codex if needed for a newly installed skill to appear.

## Adding a skill

1. Add a folder named for the skill under `skills/`, with its `SKILL.md` and any required resources.
2. Validate and try it with a realistic request.
3. Add its name, purpose, and link to the skills index above.
4. Review all files for private information, credentials, and third-party material before publishing.

## License

No license has been selected yet. Public visibility alone does not grant permission to reuse the contents; a license can be added when the owner chooses one.

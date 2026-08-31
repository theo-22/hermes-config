# Skills Repo Notes

Run `./install-hooks` after cloning `~/Skills/` to reinstall the local pre-commit hook that checks `SKILL_INDEX.md` against the live skill directories.

`./skills-card-check` validates YAML, required shared metadata, index membership, and Codex exposure. Install its parser with `python3 -m pip install -r requirements.txt` in the interpreter environment used by the checker.

Keep `name` and `description` at the top level. Put the four required library fields and other library extensions under the standard `metadata` mapping so the same file works with Codex's generic `skill-creator/scripts/quick_validate.py`:

```yaml
---
name: example-skill
description: Describe what the skill does and when to use it.
metadata:
  category: meta
  write_mode: file
  one_line_use: describe the single useful action
  fast_pick: "yes"
---
```

All six required values must be non-empty strings. Quote `"yes"` and `"no"` so YAML does not turn them into booleans. The checker rejects malformed YAML, duplicate keys, misplaced fields, and unsupported top-level extensions. Optional top-level fields are `license` and `allowed-tools`; library extensions such as tags, status, version, and owner belong under `metadata`.

Run `python3 -m unittest test_skills_card_check.py` and `./skills-card-check`. Also run the installed generic validator on changed skills: it checks generic skill constraints; the shared checker adds library routing, index, and exposure requirements. Neither proves fresh runtime discovery. Do not patch the bundled validator or remove required fields to make either check pass.

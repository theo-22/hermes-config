"""Regression coverage for shared metadata and generic-validator compatibility."""

from pathlib import Path
import runpy
import tempfile
import unittest

CHECKER = runpy.run_path(str(Path(__file__).with_name("skills-card-check")))
VALID = '''---
name: example-skill
description: >-
  Check a description: with punctuation
  and a folded continuation.
metadata:
  category: meta
  write_mode: file
  one_line_use: "keep required routing: intact"
  fast_pick: "yes"
  tags: [shared, codex]
---

# Example

Use the shared procedure.
'''


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / "example-skill"
        self.skill.mkdir()
        self.file = self.skill / "SKILL.md"

    def errors(self, text):
        self.file.write_text(text)
        return CHECKER["validate_skill_metadata"](self.root)

    def test_nested_metadata_and_folded_description(self):
        self.assertEqual(self.errors(VALID), [])
        data = CHECKER["parse_frontmatter"](self.file)
        self.assertEqual(data["description"],
                         "Check a description: with punctuation and a folded continuation.")

    def test_generic_validator_accepts_same_file(self):
        generic = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
        if not generic.is_file():
            self.skipTest("installed Codex generic validator unavailable")
        self.assertEqual(self.errors(VALID), [])
        valid, message = runpy.run_path(str(generic))["validate_skill"](self.skill)
        self.assertTrue(valid, message)

    def test_legacy_fields_require_migration(self):
        self.assertIn("move library fields under metadata",
                      self.errors(VALID.replace("metadata:\n", "category: meta\nmetadata:\n"))[0])

    def test_malformed_yaml_is_not_flattened(self):
        self.assertTrue(self.errors(VALID.replace('"keep required routing: intact"',
                                                  'keep required routing: intact')))

    def test_duplicate_fields_at_either_level(self):
        for old, new in [("name: example-skill", "name: wrong\nname: example-skill"),
                         ("  category: meta", "  category: gpt\n  category: meta")]:
            with self.subTest(old=old):
                self.assertIn("duplicate YAML key", self.errors(VALID.replace(old, new))[0])

    def test_boolean_and_non_string_required_fields(self):
        for value in ['yes', 'true', '[]', '{}', '42', '"   "', 'null']:
            with self.subTest(value=value):
                self.assertTrue(self.errors(VALID.replace('fast_pick: "yes"', f'fast_pick: {value}')))

    def test_wrong_metadata_shape(self):
        self.assertIn("metadata must be a YAML mapping", self.errors(
            '---\nname: example-skill\ndescription: Check it\nmetadata: []\n---\n')[0])

    def test_nested_extension_cannot_supply_required_field(self):
        self.assertTrue(self.errors(VALID.replace('  category: meta',
                                                   '  extension:\n    category: meta')))

    def test_name_cannot_be_shadowed(self):
        self.assertTrue(self.errors(VALID.replace('metadata:', 'metadata:\n  name: example-skill')))

    def test_required_fields_and_enums_remain_enforced(self):
        for key in CHECKER['REQUIRED_METADATA']:
            with self.subTest(key=key):
                lines = VALID.splitlines()
                lines = [line for line in lines if not line.lstrip().startswith(key + ':')]
                self.assertTrue(self.errors('\n'.join(lines) + '\n'))
        for old, new in [('category: meta', 'category: file-write'),
                         ('write_mode: file', 'write_mode: anything'),
                         ('fast_pick: "yes"', 'fast_pick: "maybe"')]:
            with self.subTest(old=old):
                self.assertTrue(self.errors(VALID.replace(old, new)))

    def test_malformed_header_and_non_mapping(self):
        for text in ['# No header', '---\n[]\n---\n', '---\nname: example-skill']:
            with self.subTest(text=text):
                self.assertTrue(self.errors(text))


if __name__ == '__main__':
    unittest.main()

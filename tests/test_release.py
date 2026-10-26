from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'tools/build_release.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ReleaseTests(unittest.TestCase):
    def test_archives_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            manifest = builder.build(ROOT, target, 'v1.0.0')
            for package in manifest['packages']:
                archive = target / package['file']
                self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), package['sha256'])
                with zipfile.ZipFile(archive) as zf:
                    expected = {f['path']: f['sha256'] for f in package['files']}
                    self.assertEqual(set(zf.namelist()), set(expected))
                    self.assertIn(package['name'] + '/SKILL.md', expected)
                    self.assertIsNone(zf.testzip())
                    for member, digest in expected.items():
                        self.assertEqual(hashlib.sha256(zf.read(member)).hexdigest(), digest)
                        self.assertFalse(member.endswith('.py'))

    def test_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / 'a', Path(tmp) / 'b'
            self.assertEqual(builder.build(ROOT, a, 'v1.0.0'), builder.build(ROOT, b, 'v1.0.0'))
            for p in a.iterdir():
                self.assertEqual(p.read_bytes(), (b / p.name).read_bytes())

    def check_mutation(self, change: str, content: str, expected: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'skills', root / 'skills')
            path = root / 'skills/chancharts-research' / change
            path.write_text(content, encoding='utf-8')
            with self.assertRaisesRegex(ValueError, expected):
                builder.build(root, root / 'dist', 'v1.0.0')
            self.assertFalse((root / 'dist').exists())

    def test_missing_reference(self) -> None:
        self.check_mutation('references/broken.md', '[missing](not-present.md)', 'broken_or_escaping_reference')

    def test_escape_reference(self) -> None:
        self.check_mutation('references/escape.md', '[outside](../../chancharts-automation/SKILL.md)', 'broken_or_escaping_reference')

    def test_secret_rejected(self) -> None:
        self.check_mutation('references/secret.md', 'ccmcp_' + 'a' * 32, 'private_content_pattern')

    def test_executable_rejected(self) -> None:
        self.check_mutation('install.py', 'raise RuntimeError()', 'unexpected_skill_resource')

    def test_bad_frontmatter_rejected(self) -> None:
        self.check_mutation('SKILL.md', '---\nname: wrong\ndescription: text\n---\n', 'invalid_skill_frontmatter')

    def test_bad_version_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'invalid_release_version'):
                builder.build(ROOT, Path(tmp) / 'out', '../bad')


if __name__ == '__main__':
    unittest.main()

"""Validate the allowlisted public Skills and build deterministic ZIP packages."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

NAMES = ('chancharts-research', 'chancharts-deep-review', 'chancharts-automation')
SENSITIVE = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----|ccmcp_[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/opt/chancharts/|/var/lib/chancharts)')
LINK = re.compile(r'\]\(([^)]+)\)')


def skill_files(root: Path, name: str) -> list[Path]:
    """Return only self-contained, regular public instruction resources."""
    folder = root / 'skills' / name
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('invalid_skill_folder')
    folder = folder.resolve()
    files = []
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError('symlink_not_allowed')
        if path.is_dir():
            continue
        rel = path.relative_to(folder)
        if rel.as_posix() != 'SKILL.md' and not (len(rel.parts) == 2 and rel.parts[0] == 'references' and path.suffix in {'.md', '.json'}):
            raise ValueError('unexpected_skill_resource')
        text = path.read_text(encoding='utf-8')
        if SENSITIVE.search(text):
            raise ValueError('private_content_pattern')
        if path.suffix == '.json':
            json.loads(text)
        else:
            for link in LINK.findall(text):
                if re.match(r'https?://', link) or link.startswith('#'):
                    continue
                target = (path.parent / link.split('#', 1)[0]).resolve()
                if not target.is_relative_to(folder) or not target.is_file():
                    raise ValueError('broken_or_escaping_reference')
        files.append(path)
    entry = folder / 'SKILL.md'
    if entry not in files:
        raise ValueError('missing_skill_entry')
    match = re.match(r'^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', entry.read_text(encoding='utf-8'))
    if not match or match[1] != name:
        raise ValueError('invalid_skill_frontmatter')
    return files


def build(root: Path, output: Path, version: str) -> dict:
    """Build all three fixed packages with stable metadata and exact content hashes."""
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+', version):
        raise ValueError('invalid_release_version')
    root = root.resolve()
    groups = {name: skill_files(root, name) for name in NAMES}
    output.mkdir(parents=True, exist_ok=True)
    manifest = {'version': version, 'real_workbuddy_zip_import': 'NOT_VERIFIED', 'packages': []}
    sums = []
    for name, files in groups.items():
        archive = output / f'{name}.zip'
        entries = []
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for path in files:
                data = path.read_bytes()
                member = f'{name}/{path.relative_to(root / "skills" / name).as_posix()}'
                info = zipfile.ZipInfo(member, (2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                zf.writestr(info, data)
                entries.append({'path': member, 'sha256': hashlib.sha256(data).hexdigest()})
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        manifest['packages'].append({'name': name, 'file': archive.name, 'sha256': digest, 'files': entries})
        sums.append(f'{digest}  {archive.name}')
    (output / 'RELEASE_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'SHA256SUMS.txt').write_text('\n'.join(sums) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    result = build(repo, args.output or repo / 'dist', args.version)
    print(json.dumps({'version': result['version'], 'packages': len(result['packages'])}))

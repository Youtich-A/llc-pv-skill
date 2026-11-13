"""Install the complete skill locally. Dry-run by default; no downloads or host edits."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

sys.dont_write_bytecode = True
from check_release import inspect

NAME = 'llc-pv-skill'
SOURCE = Path(__file__).resolve().parents[1]


def digests(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-dir', type=Path, required=True,
                        help='Actual skill search directory of the receiving host')
    parser.add_argument('--apply', action='store_true', help='Write files; default only prints plan')
    parser.add_argument('--replace', action='store_true', help='Back up and replace this skill only')
    args = parser.parse_args()
    source = SOURCE.resolve()
    skills = args.skills_dir.expanduser().resolve()
    target = skills / NAME
    if skills == Path(skills.anchor):
        parser.error('Choose a dedicated skill directory, not a filesystem root')
    if source.is_relative_to(skills) or skills.is_relative_to(source):
        parser.error('Source and target skill directories must be separate')
    if target.is_symlink() or target.exists() and not target.is_dir():
        parser.error('Destination must be an ordinary directory, not a symlink or file')
    report = inspect(source, allow_git_metadata=True)
    if report['findings']:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        parser.error('Source failed release checks; no installation performed')
    if target.exists() and not args.replace:
        parser.error('Destination exists; inspect it first, then use --replace to back it up')
    plan = {'source': str(source), 'target': str(target), 'apply': args.apply,
            'replace': args.replace, 'network_access': False, 'host_config_changes': False}
    if not args.apply:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    skills.mkdir(parents=True, exist_ok=True)
    backup_root = skills.parent / 'skill-install-backups'
    if backup_root.resolve().is_relative_to(skills):
        parser.error('Backup location must stay outside the active skill search directory')
    backup = None
    # TemporaryDirectory owns cleanup of this fresh, bounded staging path only.
    with tempfile.TemporaryDirectory(prefix='.llc-skill-install-', dir=skills.parent) as td:
        staged = Path(td) / NAME
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns('.git'))
        expected = digests(source)
        if expected != digests(staged) or inspect(staged)['findings']:
            raise RuntimeError('Staged payload did not verify; original installation kept')
        if target.exists():
            # Exact resolved target is verified before moving a directory on Windows.
            if target.resolve() != skills / NAME or target.name != NAME:
                raise RuntimeError('Unexpected replacement target')
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup = backup_root / (NAME + '-' + stamp + '-' + uuid.uuid4().hex[:8])
            if not backup.resolve().is_relative_to(backup_root.resolve()):
                raise RuntimeError('Unexpected backup target')
            target.rename(backup)
        try:
            staged.rename(target)
            if expected != digests(target):
                raise RuntimeError('Installed payload hash mismatch')
        except Exception:
            if target.exists():
                if target.resolve() != skills / NAME:
                    raise RuntimeError('Cannot roll back an unexpected target')
                target.rename(Path(td) / 'failed-payload')
            if backup is not None:
                backup.rename(target)
            raise
    plan.update(installed=True, files_verified=len(expected), backup=str(backup) if backup else None)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

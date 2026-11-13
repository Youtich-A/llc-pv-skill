"""Offline heuristic release check. Prints locations, never suspected secret values."""
import argparse
import hashlib
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {'.md', '.py', '.json', '.yaml', '.yml', '.txt', '.toml'}
PRIVATE_PATTERNS = {
    'user_home_path': re.compile(r'(?:[A-Za-z]:[\\/]+Users[\\/]+[^\s\\/]+|/(?:Users|home)/[^\s/]+)'),
    'private_key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'api_secret': re.compile(r'\bsk-[A-Za-z0-9_-]{24,}\b'),
    'aws_access_key': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'email_candidate': re.compile(r'\b[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
}
PRIVATE_PATTERNS.update({
    'private_endpoint': re.compile(r'https?://(?:10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(?=[:/\s]|$)'),
    'url_credentials': re.compile(r'https?://[^/\s:@]+:[^/\s@]+@'),
    'bearer_credential': re.compile(r'\bBearer\s+[A-Za-z0-9._~-]{20,}', re.I),
    'secret_assignment': re.compile(r'''\b(?:password|passwd|api_key|access_token|client_secret)["']?\s*[:=]\s*["'][^"'<>\s]{6,}["']''', re.I),
})
FORBIDDEN_DIRS = {'.git', 'node_modules', '__pycache__', 'runtime', 'local'}
FORBIDDEN_SUFFIXES = {'.aep', '.aepx', '.mp4', '.mov', '.wav', '.mp3', '.zip', '.skill', '.log', '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.exe', '.dll', '.ttf', '.otf', '.ttc', '.pfx', '.pem', '.psd', '.psb', '.psd2live', '.cmo3', '.moc3', '.blend', '.glb'}
FORBIDDEN_NAMES = {'vw.config.json', 'credentials.json', 'auth.json', 'cookies.txt'}


def inspect(root, deny_terms=(), verify_manifest=False, allow_git_metadata=False):
    root = Path(root).resolve()
    findings = []
    count = 0
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if allow_git_metadata and '.git' in rel.parts:
            continue
        if path.is_symlink():
            findings.append({'file': rel.as_posix(), 'kind': 'symlink'})
            continue
        if path.is_dir() and path.name in FORBIDDEN_DIRS:
            findings.append({'file': rel.as_posix(), 'kind': 'excluded_release_directory'})
        if not path.is_file():
            continue
        count += 1
        if any(x in FORBIDDEN_DIRS for x in rel.parts) or path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name in FORBIDDEN_NAMES or '.local.' in path.name or path.name.startswith('.env') and path.name != '.env.example':
            findings.append({'file': rel.as_posix(), 'kind': 'excluded_release_file'})
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {'LICENSE', '.gitignore'}:
            findings.append({'file': rel.as_posix(), 'kind': 'unexpected_payload_type'})
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            findings.append({'file':rel.as_posix(), 'kind':'non_utf8_payload'})
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(line):
                    findings.append({'file': rel.as_posix(), 'line': number, 'kind': kind})
            for term in deny_terms:
                if term.casefold() in line.casefold():
                    findings.append({'file':rel.as_posix(), 'line':number, 'kind':'private_deny_term'})
            # OS-distributed font locations are portable candidates, not user profiles.
            if any(not line[m.start():].startswith('C:/Windows/Fonts/')
                   for m in re.finditer(r'\b[A-Za-z]:[\\/]', line)):
                findings.append({'file':rel.as_posix(), 'line':number, 'kind':'machine_drive_path'})
        if path.suffix.lower() == '.md':
            for link in re.findall(r'\]\(([^)]+)\)', text):
                if '://' in link or link.startswith('#'):
                    continue
                target = (path.parent / link.split('#')[0].strip('<>')).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    findings.append({'file':rel.as_posix(), 'kind':'missing_or_external_relative_link'})
        if path.suffix == '.json':
            try:
                json.loads(text)
            except ValueError:
                findings.append({'file':rel.as_posix(), 'kind':'invalid_json'})
        if path.suffix == '.py':
            try:
                compile(text, str(rel), 'exec')
            except SyntaxError:
                findings.append({'file':rel.as_posix(), 'kind':'invalid_python'})
    entry = root / 'SKILL.md'
    if not entry.is_file():
        findings.append({'file':'SKILL.md', 'kind':'missing_entrypoint'})
    else:
        header = entry.read_text(encoding='utf8').split('---', 2)
        if len(header) < 3 or not re.search(r'^name: llc-pv-skill\s*$', header[1], re.M) or not re.search(r'^description: .+', header[1], re.M):
            findings.append({'file':'SKILL.md', 'kind':'nonstandard_skill_metadata'})
    manifest = root / 'release_manifest.json'
    if verify_manifest:
        try:
            expected = json.loads(manifest.read_text(encoding='utf8'))['files']
            actual = {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in root.rglob('*') if p.is_file() and p != manifest and not p.is_symlink() and not (allow_git_metadata and '.git' in p.relative_to(root).parts)}
            if expected != actual:
                findings.append({'file':'release_manifest.json', 'kind':'payload_hash_mismatch'})
        except (OSError, ValueError, KeyError, TypeError):
            findings.append({'file':'release_manifest.json', 'kind':'invalid_or_missing_manifest'})
    return {'files_scanned': count, 'findings':findings,
            'limits':'Heuristic only. Review names, content rights, archive membership and Git history manually. No network or AE calls.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--deny-term', action='append', default=[], help='Private audit term; values are never echoed')
    p.add_argument('--verify-manifest', action='store_true', help='Verify exact release file membership and SHA-256')
    p.add_argument('--git-worktree', action='store_true', help='Skip .git metadata only; does not audit Git history')
    args = p.parse_args()
    root = args.directory.resolve()
    if not root.is_dir():
        p.error('directory must exist')
    result = inspect(root, args.deny_term, args.verify_manifest, args.git_worktree)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['findings'] else 0


if __name__ == '__main__':
    raise SystemExit(main())

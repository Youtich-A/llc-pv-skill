"""Validate declared three-round coverage; does not verify visual truth or run video tools."""
import argparse
import json
import math
from pathlib import Path


def interval(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError('expected a [start,end] interval')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in value):
        raise ValueError('interval endpoints must be finite numbers')
    if value[0] >= value[1]:
        raise ValueError('interval must have positive duration')
    return value


def covered(windows, target):
    if not isinstance(windows, list):
        return False
    try:
        spans = sorted(interval(x) for x in windows)
    except (ValueError, TypeError):
        return False
    cursor = target[0]
    for start, end in spans:
        if end <= cursor:
            continue
        if start > cursor + 1e-6:
            return False
        cursor = max(cursor, end)
    return cursor >= target[1] - 1e-6


def validate(data, base):
    errors = []
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        return ['invalid record/schema_version']
    try:
        reference = interval(data['reference_range'])
        output = interval(data['segment_range'])
    except (ValueError, TypeError, KeyError):
        return ['missing or invalid reference_range/segment_range']
    if output[0] < reference[0] or output[1] > reference[1]:
        errors.append('segment_range outside reference_range')
    latest = data.get('latest_render_version')
    shots = data.get('shot_ids')
    if not isinstance(latest, str) or not latest.strip():
        errors.append('missing latest_render_version')
    if not isinstance(shots, list) or not shots or any(not isinstance(x, str) or not x.strip() for x in shots):
        return errors + ['shot_ids must list every current segment shot']
    if len(set(shots)) != len(shots):
        errors.append('duplicate shot_ids')
    rounds = data.get('rounds')
    if not isinstance(rounds, list) or len(rounds) != 3:
        return errors + ['exactly three round records required']
    base = Path(base).resolve()
    for number, record in enumerate(rounds, 1):
        prefix = f'round {number}: '
        if not isinstance(record, dict):
            errors.append(prefix + 'invalid record')
            continue
        if record.get('number') != number:
            errors.append(prefix + 'wrong execution order')
        if record.get('status') != 'passed':
            errors.append(prefix + 'not passed')
        if record.get('output_version') != latest:
            errors.append(prefix + 'coverage/regression not confirmed for latest output')
        if not isinstance(record.get('reference_invocation'), str) or not record['reference_invocation'].strip():
            errors.append(prefix + 'missing this round video-watch invocation')
        if not covered(record.get('reference_viewed_ranges'), reference):
            errors.append(prefix + 'reference coverage gap')
        if not covered(record.get('output_viewed_ranges'), output):
            errors.append(prefix + 'output coverage gap')
        seen = record.get('shots')
        if not isinstance(seen, list) or any(not isinstance(x, str) for x in seen) or set(seen) != set(shots) or len(seen) != len(shots):
            errors.append(prefix + 'shot coverage incomplete/duplicate')
        issues = record.get('issues')
        if not isinstance(issues, list):
            errors.append(prefix + 'missing complete issue list (empty allowed)')
            issues = []
        issue_ids = set()
        for issue in issues:
            if not isinstance(issue, dict) or not isinstance(issue.get('id'), str) or not issue['id'].strip():
                errors.append(prefix + 'invalid issue record')
                continue
            if issue['id'] in issue_ids:
                errors.append(prefix + 'duplicate issue id')
            issue_ids.add(issue['id'])
            if issue.get('status') not in ('closed', 'accepted_difference'):
                errors.append(prefix + 'unresolved issue')
            if issue.get('status') == 'accepted_difference' and not issue.get('authorization'):
                errors.append(prefix + 'difference missing user authorization')
        evidence = record.get('evidence')
        roles = set()
        if not isinstance(evidence, list):
            evidence = []
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(prefix + 'invalid evidence record')
                continue
            path = item.get('path')
            if not isinstance(path, str) or not path.strip():
                errors.append(prefix + 'missing evidence path')
                continue
            rel = Path(path)
            resolved = (base / rel).resolve()
            if rel.is_absolute() or not resolved.is_relative_to(base) or not resolved.is_file():
                errors.append(prefix + 'evidence must be an existing project-relative file')
                continue
            if item.get('viewed') is not True:
                errors.append(prefix + 'generated/measured evidence not declared viewed')
                continue
            role = item.get('role')
            if isinstance(role, str):
                roles.add(role)
            else:
                errors.append(prefix + 'invalid evidence role')
        if not {'reference', 'output', 'manifest'}.issubset(roles):
            errors.append(prefix + 'missing reference/output/manifest evidence')
        if issues and not record.get('regression_evidence'):
            errors.append(prefix + 'missing post-fix regression evidence')
        for field in ['regression_evidence']:
            path = record.get(field)
            if path:
                if not isinstance(path, str):
                    errors.append(prefix + 'invalid regression path')
                else:
                    rel = Path(path); resolved = (base / rel).resolve()
                    if rel.is_absolute() or not resolved.is_relative_to(base) or not resolved.is_file():
                        errors.append(prefix + 'regression evidence file missing/outside project')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path, help='Project-local review_execution.json; paths relative to its folder')
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding='utf-8'))
        errors = validate(data, args.record.parent)
    except (OSError, ValueError):
        errors = ['record unreadable or invalid JSON']
    print(json.dumps({'declaration_consistent': not errors, 'errors': errors,
                      'limit': 'Checks declarations and file existence only; not proof of viewing, visual correctness, or user acceptance.'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())

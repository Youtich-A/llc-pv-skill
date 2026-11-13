"""Read-only RGBA sequence audit. Requires Pillow and NumPy; never edits inputs."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--glob', default='*.png')
    p.add_argument('--fps', type=float, default=30)
    p.add_argument('--expected-count', type=int)
    p.add_argument('--allow-hold', action='append', default=[], metavar='FIRST:LAST',
                   help='Inclusive file-number range allowed to duplicate the previous frame; repeatable.')
    p.add_argument('--out', type=Path, help='Optional new JSON report; existing files are not overwritten.')
    p.add_argument('--strict', action='store_true', help='Exit 2 for missing numbers, size changes, count mismatch or unexpected duplicates.')
    args = p.parse_args()
    if not args.directory.is_dir() or args.fps <= 0:
        p.error('directory must exist and fps must be positive')
    if args.out and args.out.exists():
        p.error('report already exists; choose another output path')
    allowed = set()
    for span in args.allow_hold:
        try:
            a, b = map(int, span.split(':'))
            if a > b:
                raise ValueError()
            allowed.update(range(a, b + 1))
        except ValueError:
            p.error('--allow-hold expects an inclusive FIRST:LAST range')
    numbered = []
    for path in args.directory.glob(args.glob):
        if path.is_file():
            m = re.search(r'(\d+)$', path.stem)
            if not m:
                p.error('matching filenames must end with a frame number: ' + path.name)
            numbered.append((int(m.group()), path))
    numbered.sort(key=lambda x: (x[0], x[1].name))
    if not numbered:
        p.error('no matching frames')
    nums = [n for n, _ in numbered]
    missing = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums))
    repeated_numbers = sorted(n for n in set(nums) if nums.count(n) > 1)
    rows, previous, previous_hash, sizes = [], None, None, set()
    duplicates, empty = [], []
    for number, path in numbered:
        with Image.open(path) as image:
            sizes.add(image.size)
            rgba = np.array(image.convert('RGBA'), dtype=np.uint16)
        alpha = rgba[:, :, 3]
        premult = np.concatenate((rgba[:, :, :3] * alpha[:, :, None],
                                 alpha[:, :, None] * 255), axis=2)
        digest = hashlib.sha256(premult.tobytes()).hexdigest()
        duplicate = previous_hash == digest
        if duplicate:
            duplicates.append(number)
        ys, xs = np.nonzero(alpha)
        if not len(xs):
            empty.append(number)
        row = {'frame': number, 'file': path.name,
               'alpha_bbox_xyxy_exclusive': [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None,
               'alpha_mean_0_255': float(alpha.mean()),
               'duplicate_of_previous': duplicate,
               'mean_premultiplied_difference_0_255': float(np.abs(premult.astype(np.int32) - previous).mean() / 255) if previous is not None and previous.shape == premult.shape else None}
        rows.append(row)
        previous, previous_hash = premult.astype(np.int32), digest
    unexpected = [n for n in duplicates if n not in allowed]
    mismatch = args.expected_count is not None and len(numbered) != args.expected_count
    report = {'directory': str(args.directory.resolve()), 'fps': args.fps,
              'frames': len(numbered), 'first': nums[0], 'last': nums[-1],
              'observed_duration_seconds': len(numbered) / args.fps,
              'sizes': [list(s) for s in sorted(sizes)], 'missing_numbers': missing,
              'repeated_frame_numbers': repeated_numbers, 'count_mismatch': mismatch,
              'duplicates': duplicates, 'unexpected_duplicates': unexpected,
              'fully_transparent_frames': empty,
              'limits': 'Duplicates include alpha and premultiplied RGB; hidden RGB does not count. No duplicates does not establish correct motion or likeness. Missing leading/trailing frames require expected-count or an external frame contract.',
              'rows': rows}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in report.items() if k != 'rows'}, ensure_ascii=False, indent=2))
    return 2 if args.strict and (missing or repeated_numbers or len(sizes) != 1 or mismatch or unexpected) else 0


if __name__ == '__main__':
    raise SystemExit(main())

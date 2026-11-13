import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class InstallerTests(unittest.TestCase):
    def test_clone_dry_run_install_and_backup_without_git_metadata(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            source = root / 'repo'
            (source / 'scripts').mkdir(parents=True)
            (source / '.git').mkdir()
            (source / '.git' / 'config').write_text('synthetic metadata', encoding='utf8')
            (source / 'SKILL.md').write_text('---\nname: llc-pv-skill\ndescription: Test workflow\n---\n', encoding='utf8')
            original = Path(__file__).resolve().parents[1] / 'scripts'
            for name in ['install_skill.py', 'check_release.py']:
                shutil.copy2(original / name, source / 'scripts' / name)
            target_root = root / 'host' / 'skills'
            args = [sys.executable, '-B', str(source / 'scripts' / 'install_skill.py'), '--skills-dir', str(target_root)]
            def run(extra=()):
                return subprocess.run(args + list(extra), capture_output=True, text=True, encoding='utf8')
            dry = run()
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse(target_root.exists())
            result = run(['--apply'])
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = target_root / 'llc-pv-skill'
            self.assertTrue((installed / 'SKILL.md').is_file())
            self.assertFalse((installed / '.git').exists())
            self.assertNotEqual(run(['--apply']).returncode, 0)
            (source / 'new.txt').write_text('new version', encoding='utf8')
            updated = run(['--apply', '--replace'])
            self.assertEqual(updated.returncode, 0, updated.stderr)
            backup = Path(json.loads(updated.stdout)['backup'])
            self.assertTrue(backup.is_dir())
            self.assertFalse(backup.is_relative_to(target_root))
            self.assertFalse((backup / 'new.txt').exists())
            self.assertTrue((installed / 'new.txt').exists())


if __name__ == '__main__':
    unittest.main()

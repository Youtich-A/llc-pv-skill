import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_release import inspect


class ReleaseBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.root = Path(self.work.name)
        (self.root / 'SKILL.md').write_text('---\nname: llc-pv-skill\ndescription: Test workflow\n---\n', encoding='utf8')

    def tearDown(self):
        self.work.cleanup()

    def test_clean_payload(self):
        self.assertEqual(inspect(self.root)['findings'], [])

    def test_git_metadata_opt_in(self):
        (self.root / '.git').mkdir()
        (self.root / '.git' / 'config').write_text('synthetic fixture', encoding='utf8')
        self.assertTrue(inspect(self.root)['findings'])
        self.assertEqual(inspect(self.root, allow_git_metadata=True)['findings'], [])

    def test_user_model_not_allowed_even_in_git_mode(self):
        for ext in ['psd', 'psd2live', 'moc3']:
            (self.root / ('character.' + ext)).write_text('synthetic fixture', encoding='utf8')
        findings = inspect(self.root, allow_git_metadata=True)['findings']
        self.assertTrue(all(any(x['file'] == 'character.' + ext for x in findings) for ext in ['psd', 'psd2live', 'moc3']))


if __name__ == '__main__':
    unittest.main()

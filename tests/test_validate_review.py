"""Synthetic evidence fixtures test bookkeeping, never actual video quality."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate_review import validate, covered


class ReviewContractTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.base = Path(self.work.name)
        for name in ['source.txt', 'output.txt', 'manifest.json', 'regression.txt']:
            (self.base / name).write_text('synthetic fixture', encoding='utf8')
        self.record = {'schema_version': 1, 'reference_range': [0, 80], 'segment_range': [0, 20],
                       'latest_render_version': 'v4', 'shot_ids': ['S001', 'S002'], 'rounds': []}
        for n in range(1, 4):
            self.record['rounds'].append({'number': n, 'status': 'passed', 'output_version': 'v4',
                'reference_invocation': f'synthetic round {n}', 'reference_viewed_ranges': [[0, 40], [40, 80]],
                'output_viewed_ranges': [[0, 20]], 'shots': ['S001', 'S002'], 'issues': [],
                'evidence': [{'path': path, 'role': role, 'viewed': True} for path, role in
                             [('source.txt', 'reference'), ('output.txt', 'output'), ('manifest.json', 'manifest')]],
                'regression_evidence': None})

    def tearDown(self):
        self.work.cleanup()

    def test_complete_declarations(self):
        self.assertEqual(validate(self.record, self.base), [])

    def test_missing_time_window(self):
        self.record['rounds'][1]['reference_viewed_ranges'] = [[0, 39], [40, 80]]
        self.assertTrue(any('coverage gap' in x for x in validate(self.record, self.base)))

    def test_old_output_and_missing_shot(self):
        self.record['rounds'][2].update(output_version='v3', shots=['S001'])
        errors = validate(self.record, self.base)
        self.assertTrue(any('latest' in x for x in errors))
        self.assertTrue(any('shot coverage' in x for x in errors))

    def test_unresolved_issue_and_regression(self):
        self.record['rounds'][0]['issues'] = [{'id': 'I1', 'status': 'pending'}]
        errors = validate(self.record, self.base)
        self.assertTrue(any('unresolved' in x for x in errors))
        self.assertTrue(any('regression' in x for x in errors))
        self.record['rounds'][0]['issues'][0]['status'] = 'closed'
        self.record['rounds'][0]['regression_evidence'] = 'regression.txt'
        self.assertEqual(validate(self.record, self.base), [])

    def test_missing_or_unviewed_evidence(self):
        self.record['rounds'][0]['evidence'][0]['viewed'] = False
        self.record['rounds'][1]['evidence'][0]['path'] = 'does-not-exist.png'
        self.assertTrue(validate(self.record, self.base))

    def test_user_authorization_required_for_retained_difference(self):
        item = self.record['rounds'][0]
        item['issues'] = [{'id': 'I1', 'status': 'accepted_difference'}]
        item['regression_evidence'] = 'regression.txt'
        self.assertTrue(any('authorization' in x for x in validate(self.record, self.base)))

    def test_malformed_data_and_non_finite_ranges(self):
        for data in [None, [], {}, {'schema_version': 1, 'reference_range': [0, float('nan')]}]:
            self.assertTrue(validate(data, self.base))
        self.assertFalse(covered([[0, float('inf')]], [0, 20]))

    def test_pending_template_cannot_pass(self):
        self.record['rounds'][0]['status'] = 'pending'
        self.assertTrue(validate(self.record, self.base))

    def test_path_escape(self):
        self.record['rounds'][0]['evidence'][0]['path'] = '../outside.png'
        self.assertTrue(validate(self.record, self.base))

    def test_malformed_evidence_role(self):
        self.record['rounds'][0]['evidence'][0]['role'] = []
        self.assertTrue(validate(self.record, self.base))


if __name__ == '__main__':
    unittest.main()

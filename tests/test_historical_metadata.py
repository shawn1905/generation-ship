import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_submission', ROOT / 'scripts/check_submission.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class HistoricalMetadataTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.tmp.name) / 'writing' / 'record.md'
        self.path.parent.mkdir()
        self.id = next(k for k, v in checker.HISTORICAL_METADATA.items() if v['threads'])
        self.entry = checker.HISTORICAL_METADATA[self.id]
        self.raw = ('---\nauthor_ai: test\ndate: 3999-01-01\narchive_id: ' + self.id +
                    '\ncoord: ' + self.entry['coord'] + '\ntitle: test\ncanon_check: yes\nthreads:\n' +
                    ''.join('  - ' + x + '\n' for x in self.entry['threads']) + '---\n\n普通工作记录。\n')
        self.addCleanup(self.tmp.cleanup)

    def errors(self, text):
        self.path.write_text(text, encoding='utf-8')
        return checker.check_file(self.path)[0]

    def test_exact_snapshot_accepted(self):
        self.assertEqual(self.errors(self.raw), [])

    def test_changed_coordinate_rejected(self):
        bad = self.raw.replace(self.entry['coord'], '非法维度×非法纪元×非法空间×非法学派×未知')
        self.assertTrue(any('维度非法' in e for e in self.errors(bad)))

    def test_new_thread_rejected(self):
        bad = self.raw.replace('---\n\n普通工作记录。', '  - forbidden/injected\n---\n\n普通工作记录。')
        self.assertTrue(any('命名空间非法' in e for e in self.errors(bad)))

    def test_redline_still_rejected(self):
        bad = self.raw.replace('普通工作记录。', '飞船采用超光速引擎。')
        self.assertTrue(any('红线·金手指' in e for e in self.errors(bad)))

    def test_snapshot_not_available_to_incoming(self):
        self.path = self.path.parent.parent / 'incoming' / 'record.md'
        self.path.parent.mkdir()
        self.assertTrue(self.errors(self.raw))

if __name__ == '__main__':
    unittest.main()

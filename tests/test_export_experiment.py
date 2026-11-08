import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from export_experiment import read_snapshot, write_snapshot


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'source.local.json'
        self.source = {'model': 'PRIVATE-MODEL', 'draft_id': '8'*13, 'price': 1234.56,
                       'status': 'DONE', 'verified': True, 'missing': [],
                       'evidence': {'quality': '4.9 excellent', 'contact': 'PRIVATE-CONTACT'},
                       'stage_times': {'fields': 'basic 35.469s + logistics 24.641s',
                                       'save': '10.625s keyboard'}}
        self.manifest = {'batch_id': 'draft-batch-02', 'observation_date': '2026-11-08',
                         'products': [{'public_id': 'P01', 'kind': 'injector', 'result_path': str(self.path)}]}

    def export(self):
        self.path.write_text(json.dumps(self.source), encoding='utf-8')
        return read_snapshot(self.manifest)

    def test_allowlist_drops_private_and_unknown_fields(self):
        self.source['untrusted_extra'] = {'api_key': 'PRIVATE-KEY'}
        result = self.export(); text = json.dumps(result)
        for secret in ['PRIVATE-MODEL', '8'*13, '1234.56', 'PRIVATE-CONTACT', 'PRIVATE-KEY', str(self.path)]:
            self.assertNotIn(secret, text)
        self.assertEqual(result['products'][0]['instrumented_field_seconds'], 60.11)

    def test_missing_wall_time_is_null_not_script_time(self):
        row = self.export()['products'][0]
        self.assertIsNone(row['wall_clock_seconds'])
        self.assertEqual(row['timing_scope'], 'wall_not_recorded')
        self.assertEqual(row['save_command_seconds'], [10.625])

    def test_explicit_overlap_tag_and_elapsed_time(self):
        self.source.update(started_at='2026-11-08T10:00:00+08:00', finished_at='2026-11-08T10:30:00+08:00')
        self.manifest['products'][0]['timing_scope'] = 'overlapping_recovery_span'
        row = self.export()['products'][0]
        self.assertEqual(row['wall_clock_seconds'], 1800)
        self.assertEqual(row['relative_start_seconds'], 0)
        self.assertEqual(row['timing_scope'], 'overlapping_recovery_span')

    def test_done_without_verified_is_not_promoted(self):
        self.source['verified'] = False
        with self.assertRaises(ValueError): self.export()

    def test_missing_list_is_required(self):
        del self.source['missing']
        with self.assertRaises(ValueError): self.export()

    def test_identifiers_are_anonymous_and_unique(self):
        self.manifest['products'][0]['public_id'] = 'PRIVATE-MODEL'
        with self.assertRaises(ValueError): self.export()
        self.manifest['products'][0]['public_id'] = 'P01'
        self.manifest['products'].append(copy.deepcopy(self.manifest['products'][0]))
        with self.assertRaises(ValueError): self.export()

    def test_negative_or_timezone_free_wall_time_is_rejected(self):
        for begin, end in [('2026-11-08T11:00:00+08:00', '2026-11-08T10:00:00+08:00'),
                           ('2026-11-08T10:00:00', '2026-11-08T11:00:00')]:
            self.source.update(started_at=begin, finished_at=end)
            with self.assertRaises(ValueError): self.export()

    def test_multiple_save_durations_remain_separate(self):
        self.source['stage_times']['save'] = '10.562s + 9.125s (same draft)'
        self.assertEqual(self.export()['products'][0]['save_command_seconds'], [10.562, 9.125])

    def test_legacy_numeric_metrics_preserve_unverified_status(self):
        self.source.update(status='SAVED_UNVERIFIED', verified=False, quality_score=3.9,
                           evidence=['PRIVATE-EVIDENCE'], missing=['private issue one', 'private issue two'])
        self.source['stage_times'] = {'start': '2026-11-08T10:00:00+08:00',
            'end': '2026-11-08T10:42:30+08:00', 'basic_seconds': 31.109,
            'logistics_seconds': 20.235, 'total_minutes': 42.5}
        row = self.export()['products'][0]
        self.assertFalse(row['verified']); self.assertEqual(row['quality_score'], 3.9)
        self.assertEqual(row['missing_count'], 2); self.assertEqual(row['wall_clock_seconds'], 2550)
        self.assertEqual(row['instrumented_field_seconds'], 51.344)

    def test_reported_estimates_are_not_promoted_to_wall_time(self):
        self.source['stage_times'] = {'field_seconds': 39.266, 'logistics_seconds': 29.515,
            'save_seconds': 10.5, 'resave_seconds': 11.063, 'total_minutes_estimate': 40.0}
        row = self.export()['products'][0]
        self.assertIsNone(row['wall_clock_seconds'])
        self.assertEqual(row['save_command_seconds'], [10.5, 11.063])

    def test_json_csv_read_back_and_existing_snapshot_is_preserved(self):
        snapshot = self.export(); folder = Path(self.temp.name)/'public'
        files = write_snapshot(snapshot, folder)
        self.assertEqual(json.loads(files[0].read_text()), snapshot)
        with files[1].open(newline='') as stream:
            row = next(csv.DictReader(stream))
        self.assertEqual(row['public_id'], 'P01')
        self.assertEqual(row['wall_clock_seconds'], '')
        original = files[0].read_bytes()
        with self.assertRaises(FileExistsError): write_snapshot(snapshot, folder)
        self.assertEqual(files[0].read_bytes(), original)


if __name__ == '__main__':
    unittest.main()

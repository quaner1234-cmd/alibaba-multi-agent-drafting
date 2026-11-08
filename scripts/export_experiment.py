"""Export an allowlisted, anonymous result snapshot; never copy source JSON wholesale.

Usage: python scripts/export_experiment.py --manifest <private-manifest> --out <new-directory>
The private manifest contains batch_id, observation_date and products. Each product
has public_id (P01 etc.), kind, result_path and optionally timing_scope. Keep that
manifest outside this public repository. Outputs are create-only JSON and CSV.
"""
import argparse
import csv
from datetime import date, datetime
import json
import math
from pathlib import Path
import re


STATUSES = {'DONE', 'SAVED_UNVERIFIED', 'SAVE_UNKNOWN', 'INCOMPLETE', 'SKIPPED', 'BLOCKED'}
TIMING_SCOPES = {'wall_not_recorded', 'reported_product_span', 'overlapping_recovery_span'}
CSV_FIELDS = ['public_id', 'kind', 'status', 'verified', 'quality_score', 'missing_count',
              'image_check_level', 'wall_clock_seconds', 'relative_start_seconds',
              'timing_scope', 'instrumented_field_seconds', 'save_command_seconds']


def seconds(text):
    return [float(value) for value in re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)s\b', str(text or ''))]


def read_snapshot(manifest):
    batch = manifest['batch_id']
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,40}', batch):
        raise ValueError('Use an anonymous batch label')
    observed = date.fromisoformat(manifest['observation_date']).isoformat()
    products, starts, seen = [], [], set()
    for item in manifest['products']:
        public_id, kind = item['public_id'], item['kind']
        if not re.fullmatch(r'P\d{2}', public_id) or public_id in seen:
            raise ValueError('Public product labels must be unique P01-style aliases')
        if kind not in ('injector', 'pump', 'other'):
            raise ValueError('Use a generic product family')
        seen.add(public_id)
        data = json.loads(Path(item['result_path']).read_text(encoding='utf-8-sig'))
        status = data.get('status')
        if status not in STATUSES:
            raise ValueError('Unsupported result status')
        verified = data.get('verified') is True
        if status == 'DONE' and not verified:
            raise ValueError('DONE requires the source record to say verified')
        missing = data.get('missing')
        if not isinstance(missing, list):
            raise ValueError('An explicit missing-items list is required')
        evidence, timings = data.get('evidence') or {}, data.get('stage_times') or {}
        evidence = evidence if isinstance(evidence, dict) else {}
        quality = str(evidence.get('quality') or '')
        match = re.search(r'(?<![\d.])([0-5]\.\d)(?![\d.])', quality)
        numeric_score = data.get('quality_score')
        score = (float(numeric_score) if isinstance(numeric_score, (float, int))
                 and not isinstance(numeric_score, bool) else float(match[1]) if match else None)
        if score is not None and (not math.isfinite(score) or not 0 <= score <= 5):
            raise ValueError('Invalid platform score')
        begin = data.get('started_at') or timings.get('start')
        end = data.get('finished_at') or timings.get('end')
        wall, start = None, None
        if begin and end:
            start, finish = datetime.fromisoformat(begin), datetime.fromisoformat(end)
            if start.tzinfo is None or finish.tzinfo is None:
                raise ValueError('Recorded timestamps need explicit time zones')
            wall = int((finish-start).total_seconds())
            if wall < 0:
                raise ValueError('Negative product span')
        timing_scope = item.get('timing_scope', 'reported_product_span' if wall is not None else 'wall_not_recorded')
        if timing_scope not in TIMING_SCOPES or (wall is None) != (timing_scope == 'wall_not_recorded'):
            raise ValueError('Timing scope must match the available timestamps')
        field_values = [float(value) for value in re.findall(r'\b(?:basic|logistics)\s+(\d+(?:\.\d+)?)s\b', str(timings.get('fields') or ''))]
        if not field_values:
            field_values = [value for value in [timings.get('basic_seconds', timings.get('field_seconds')),
                                               timings.get('logistics_seconds')]
                            if isinstance(value, (float, int)) and not isinstance(value, bool)]
        save_values = seconds(timings.get('save', timings.get('save_readback')))
        if not save_values:
            save_values = [timings[key] for key in ('save_seconds', 'resave_seconds')
                           if isinstance(timings.get(key), (float, int)) and not isinstance(timings[key], bool)]
        level = data.get('image_check_level')
        level = level if level in ('light', 'strict') else 'not_recorded'
        products.append({'public_id': public_id, 'kind': kind, 'status': status,
            'verified': verified, 'quality_score': score, 'missing_count': len(missing),
            'image_check_level': level, 'wall_clock_seconds': wall,
            'relative_start_seconds': None, 'timing_scope': timing_scope,
            'instrumented_field_seconds': round(sum(field_values), 3) if field_values else None,
            'save_command_seconds': save_values})
        starts.append(start)
    origin = min((value for value in starts if value is not None), default=None)
    for product, start in zip(products, starts):
        if start is not None:
            product['relative_start_seconds'] = int((start-origin).total_seconds())
    return {'schema_version': 1, 'batch_id': batch, 'observation_date': observed,
            'record_type': 'desensitized_derived_observation',
            'evidence_boundary': 'Private executor result records; no new live platform audit or human approval inferred',
            'timing_boundary': 'Instrumented commands are partial timings; product spans may overlap; no sum or model ranking',
            'products': products}


def write_snapshot(snapshot, folder):
    folder = Path(folder)
    targets = [folder/'results.json', folder/'results.csv']
    if any(target.exists() for target in targets):
        raise FileExistsError('Snapshot exists; use a new observation directory')
    folder.mkdir(parents=True, exist_ok=True)
    with targets[0].open('x', encoding='utf-8') as out:
        json.dump(snapshot, out, ensure_ascii=False, indent=2); out.write('\n')
    with targets[1].open('x', encoding='utf-8', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in snapshot['products']:
            writer.writerow(dict(row, save_command_seconds=';'.join(map(str, row['save_command_seconds']))))
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args(argv)
    manifest = json.loads(Path(args.manifest).read_text(encoding='utf-8-sig'))
    result = read_snapshot(manifest)
    write_snapshot(result, args.out)
    print(json.dumps({'status': 'EXPORTED', 'products': len(result['products']),
                      'batch_id': result['batch_id']}))


if __name__ == '__main__':
    main()

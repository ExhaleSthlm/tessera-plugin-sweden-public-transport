"""Exercise the real Tessera mapper against Trafiklab response shapes, without secrets."""
import json
import os
from pathlib import Path
import sys
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
import yaml

ROOT = Path(__file__).resolve().parents[1]
TREE = Path(os.environ.get('TESSERA_TREE', '../homeassistant_espscreen'))
sys.path.insert(0, str(TREE / 'screen_manager/app'))
import plugin_manifest
import plugin_fetch

MANIFEST = plugin_manifest.check(yaml.safe_load((ROOT / 'tessera-plugin.yaml').read_text()),
    json.loads((ROOT / 'translations/en.json').read_text()))
SPEC = MANIFEST['fetch'][0]['map']

def departure(line='163', destination='Bredäng', time='2026-10-17T14:05:00', mode='BUS', canceled=False, rt=True):
    return {'route': {'designation': line, 'direction': destination, 'transport_mode': mode},
            'realtime': time, 'scheduled': '2026-10-17T14:04:00', 'is_realtime': rt, 'canceled': canceled}

def mapped(items, **options):
    return plugin_fetch.apply_map(SPEC, {'departures': items}, options)['items']

class MappingTests(unittest.TestCase):
    def test_two_bus_lines_both_directions_exclude_other_lines_and_cancelled(self):
        data = [departure('163', 'Bredäng'), departure('163', 'Kärrtorp'),
                departure('816', 'Tyresö centrum'), departure('816', 'Gullmarsplan'),
                departure('18', 'Alvik', mode='METRO'), departure(canceled=True)]
        result = mapped(data, line='163', line2='816', mode='BUS')
        self.assertEqual([r['to'] for r in result], ['Bredäng','Kärrtorp','Tyresö centrum','Gullmarsplan'])
    def test_metro_area_with_bus_services(self):
        result = mapped([departure(), departure('18','Farsta strand',mode='METRO'),
                         departure('18','Alvik',mode='METRO')], mode='METRO')
        self.assertEqual(len(result), 2)
        self.assertEqual({r['line'] for r in result}, {'18'})
    def test_empty_filters_include_all_and_second_line_alone_works(self):
        data = [departure('163'), departure('816')]
        self.assertEqual(len(mapped(data)),2)
        self.assertEqual([r['line'] for r in mapped(data,line2='816')],['816'])
    def test_exact_destination(self):
        result = mapped([departure(destination='Bredäng'),departure(destination='Kärrtorp')], direction='Kärrtorp')
        self.assertEqual([r['to'] for r in result], ['Kärrtorp'])
    def test_sort_before_limit_and_filter_before_limit(self):
        data = [departure('999') for _ in range(20)]
        data += [departure(time=f'2026-10-17T14:{m:02}:00') for m in range(30,10,-1)]
        result = mapped(data, line='163')
        self.assertEqual(len(result),12)
        self.assertEqual(result[0]['at'],int(datetime(2026,10,17,14,11,tzinfo=ZoneInfo('Europe/Stockholm')).timestamp()))
        self.assertEqual(result[-1]['at']-result[0]['at'],11*60)
    def test_timetable_and_cancel_booleans_are_numeric(self):
        result = mapped([departure(rt=False)])[0]
        self.assertEqual(result['rt'],0)
        self.assertEqual(result['cancel'],0)
    def test_empty_and_missing_items(self):
        self.assertEqual(mapped([]),[])
        self.assertEqual(plugin_fetch.apply_map(SPEC,{}, {})['items'],[])
    def test_winter_and_summer_local_time(self):
        for stamp in ['2026-01-17T14:05:00','2026-07-17T14:05:00']:
            actual=mapped([departure(time=stamp)])[0]['at']
            expected=int(datetime.fromisoformat(stamp).replace(tzinfo=ZoneInfo('Europe/Stockholm')).timestamp())
            self.assertEqual(actual,expected)
    def test_payload_fits_budget_at_maximum_field_lengths(self):
        data=[departure(line='x'*48,destination='å'*48) for _ in range(12)]
        payload=plugin_fetch.apply_map(SPEC,{'departures':data},{})
        self.assertLessEqual(len(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()),2600)
    def test_stop_lookup_preserves_ids_and_swedish_names(self):
        spec = next(f['map'] for f in MANIFEST['fetch'] if f['id'] == 'stops')
        choices = plugin_fetch.apply_choices(spec, {'stop_groups': [
            {'id':'740021703', 'name':'Blåsut T-bana'},
            {'id':'740065542', 'name':'Dalens sjukhus'}]})
        self.assertEqual({c['value'] for c in choices}, {'740021703','740065542'})
        self.assertTrue(any('Blåsut' in c['label'] for c in choices))

    def test_two_stop_budget_leaves_margin_in_31_day_month(self):
        interval = next(f['every'] for f in MANIFEST['fetch'] if f['id'] == 'departures')
        self.assertLess(2 * 31 * 24 * 3600 / interval, 90000)

    def test_translation_keys_match(self):
        en=json.loads((ROOT/'translations/en.json').read_text())
        sv=json.loads((ROOT/'translations/sv.json').read_text())
        for section in ('app','screen'):
            self.assertEqual(set(en[section]),set(sv[section]))

if __name__ == '__main__': unittest.main()

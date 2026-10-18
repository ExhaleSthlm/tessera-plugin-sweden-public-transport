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
from plugins import Plugins

MANIFEST = plugin_manifest.check(yaml.safe_load((ROOT / 'tessera-plugin.yaml').read_text()),
    json.loads((ROOT / 'translations/en.json').read_text()))
FETCH = next(f for f in MANIFEST['fetch'] if f['id'] == 'departures')
SPEC = FETCH['map']

def departure(line='163', destination='Bredäng', time='2026-10-17T14:05:00', mode='BUS', canceled=False, rt=True):
    return {'route': {'designation': line, 'direction': destination, 'transport_mode': mode},
            'realtime': time, 'scheduled': '2026-10-17T14:04:00', 'is_realtime': rt, 'canceled': canceled}

def picks(*lines):
    return [{'value': line, 'label': line} for line in lines]

def mapped(items, lines=('163',), **options):
    chosen = {**options, 'selected_lines': picks(*lines)}
    answers = [({'departures': items}, values, pick) for values, pick in Plugins.asks(FETCH, chosen)]
    return plugin_fetch.apply_each(SPEC, answers)['items']

class MappingTests(unittest.TestCase):
    def test_two_bus_lines_both_directions_exclude_other_lines_and_cancelled(self):
        data = [departure('163', 'Bredäng'), departure('163', 'Kärrtorp'),
                departure('816', 'Tyresö centrum'), departure('816', 'Gullmarsplan'),
                departure('18', 'Alvik', mode='METRO'), departure(canceled=True)]
        result = mapped(data, lines=('163', '816'), mode='BUS')
        self.assertEqual([r['to'] for r in result], ['Bredäng','Kärrtorp','Tyresö centrum','Gullmarsplan'])
    def test_metro_area_with_bus_services(self):
        result = mapped([departure(), departure('18','Farsta strand',mode='METRO'),
                         departure('18','Alvik',mode='METRO')], lines=('18',), mode='METRO')
        self.assertEqual(len(result), 2)
        self.assertEqual({r['line'] for r in result}, {'18'})
    def test_empty_selection_does_not_ask_or_show_unfiltered_departures(self):
        self.assertEqual(Plugins.asks(FETCH, {'selected_lines': []}), [])
        self.assertEqual(mapped([departure('163'), departure('816')], lines=()), [])
        self.assertEqual([r['line'] for r in mapped([departure('163'), departure('816')], lines=('816',))], ['816'])

    def test_all_line_picks_share_one_stop_request_and_choice_cache(self):
        chosen = {'stop': {'value': '740065542', 'label': 'Dalens sjukhus'},
                  'selected_lines': picks('163', '816')}
        requests = [plugin_fetch.fill(FETCH, values, {'api_key': 'test-key'})
                    for values, _ in Plugins.asks(FETCH, chosen)]
        choice_fetch = next(f for f in MANIFEST['fetch'] if f['id'] == 'lines')
        requests.append(plugin_fetch.fill(choice_fetch, plugin_fetch.words_of(chosen), {'api_key': 'test-key'}))
        keys = {plugin_fetch.question(MANIFEST['id'], url, headers) for url, headers in requests}
        self.assertEqual(len(keys), 1)

    def test_merged_lines_are_sorted_and_limited_together(self):
        data = [departure('163', time=f'2026-10-17T14:{m:02}:00') for m in range(12, 30, 2)]
        data += [departure('816', time=f'2026-10-17T14:{m:02}:00') for m in range(11, 30, 2)]
        result = mapped(data, lines=('163', '816'))
        self.assertEqual(len(result), 12)
        self.assertEqual([r['line'] for r in result], ['816', '163'] * 6)
        self.assertEqual(result[-1]['at'] - result[0]['at'], 11 * 60)

    def test_line_pick_validation_rejects_duplicates_and_old_scalars(self):
        option = next(o for o in MANIFEST['tiles'][0]['options'] if o['id'] == 'selected_lines')
        self.assertEqual(plugin_manifest.option_value(option, picks('163', '816')), picks('163', '816'))
        for invalid in ('163', picks('163', '163'), picks(*(str(i) for i in range(9)))):
            with self.assertRaises(plugin_manifest.ManifestError):
                plugin_manifest.option_value(option, invalid)

    def test_exact_destination(self):
        result = mapped([departure(destination='Bredäng'),departure(destination='Kärrtorp')], direction='Kärrtorp')
        self.assertEqual([r['to'] for r in result], ['Kärrtorp'])
    def test_sort_before_limit_and_filter_before_limit(self):
        data = [departure('999') for _ in range(20)]
        data += [departure(time=f'2026-10-17T14:{m:02}:00') for m in range(30,10,-1)]
        result = mapped(data, lines=('163',))
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

    def test_line_choices_deduplicate_directions_and_ignore_selected_filters(self):
        spec = next(f['map'] for f in MANIFEST['fetch'] if f['id'] == 'lines')
        choices = plugin_fetch.apply_choices(spec, {'departures': [
            departure('816', 'Tyresö centrum'), departure('163', 'Bredäng'),
            departure('163', 'Kärrtorp'), departure('816', 'Gullmarsplan'),
            departure('18', 'Alvik', mode='METRO')]}, {'line': '163', 'mode': 'BUS'})
        self.assertEqual(choices, [{'value': n, 'label': n} for n in ('18', '163', '816')])

    def test_line_choices_handle_no_departures_and_missing_designations(self):
        spec = next(f['map'] for f in MANIFEST['fetch'] if f['id'] == 'lines')
        for data in ({}, {'departures': []}, {'departures': [{'route': {}}, {}]}):
            self.assertEqual(plugin_fetch.apply_choices(spec, data), [])

    def test_two_stop_budget_leaves_margin_in_31_day_month(self):
        interval = next(f['every'] for f in MANIFEST['fetch'] if f['id'] == 'departures')
        self.assertLess(2 * 31 * 24 * 3600 / interval, 90000)

    def test_searchable_stop_keeps_label_but_fetch_uses_id(self):
        option = next(o for o in MANIFEST['tiles'][0]['options'] if o['id'] == 'stop')
        pick = plugin_manifest.option_value(option, {'value': '740021703', 'label': 'Blåsut'})
        self.assertEqual(pick['label'], 'Blåsut')
        fetch = next(f for f in MANIFEST['fetch'] if f['id'] == 'departures')
        url, headers = plugin_fetch.fill(fetch, plugin_fetch.words_of({'stop': pick}), {'api_key': 'test-key'})
        self.assertIn('/departures/740021703?', url)
        self.assertNotIn('Blåsut', url)
        self.assertEqual(headers, {})

    def test_old_scalar_stop_requires_reselection(self):
        option = next(o for o in MANIFEST['tiles'][0]['options'] if o['id'] == 'stop')
        with self.assertRaises(plugin_manifest.ManifestError):
            plugin_manifest.option_value(option, '740021703')
        self.assertEqual(plugin_manifest.option_value(option, ''), '')

    def test_translation_keys_match(self):
        en=json.loads((ROOT/'translations/en.json').read_text())
        sv=json.loads((ROOT/'translations/sv.json').read_text())
        for section in ('app','screen'):
            self.assertEqual(set(en[section]),set(sv[section]))

if __name__ == '__main__': unittest.main()

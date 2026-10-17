# Public transport (SE) for Tessera

Swedish public transport departures on Tessera ESP32 screens, using Trafiklab Timetables.
Install once and add multiple tiles, each with its own stop, up to two lines, transport mode and optional destination.
Swedish and English translations are included. This beta requires Tessera plugin API 0.10 (Tessera 0.4.88 / firmware 0.56.0 or later compatible versions).

## Set up

1. Create a key for **Trafiklab Realtime APIs** at https://developer.trafiklab.se/. A ResRobot key is a different product.
2. In Tessera, open Plugins, choose **Add with a link**, and enter https://github.com/ExhaleSthlm/tessera-plugin-sweden-public-transport.
3. Add the plugin to the intended screen and build its firmware. This updates the screen; allow time for the build.
4. Enter the API key in the plugin's secret **Trafiklab API key** input. Never put it in YAML or Git.
5. Add a **Departures** tile in Layout. Search for a stop name, leave the search field, choose a matching stop, and optionally select a transport mode, first line and second line. Both line fields empty means all lines. Destination empty means all directions.
6. Save and send the layout. Wide tiles show a departure list, including the Guition 1×3 grid; narrow tiles emphasize the next departure.

Stop groups can be found with [Trafiklab Stop Lookup](https://www.trafiklab.se/api/our-apis/trafiklab-realtime-apis/stop-lookup/).
The built-in name search stores the group ID automatically. After changing the search text, explicitly choose a new result; the previous selection is retained until then. Search results are limited to 48, so use a specific name. Choose line numbers from the dropdowns after selecting a stop. Choices include each line once across both directions, using departures in the next 60 minutes; lines without departures in that window may be absent. The choices show all transport modes at the stop; the separate transport-mode filter still controls the displayed departures. Both line choices empty means all lines. After changing stops, reselect both line choices: Tessera retains existing selections. Tessera 0.4.88 does not offer an empty/reset entry in dynamically populated dropdowns. To return to all lines after choosing a filter, create a new tile and leave its line choices untouched; to remove only the second filter, select the same line in both fields. Existing saved line numbers remain valid. Destination text must be an exact, case-sensitive match.

Example configuration, verified with Trafiklab on 2026-10-17:

| Tile | Stop ID | Mode | First line | Second line | Destination |
| --- | --- | --- | --- | --- | --- |
| Blåsut metro | `740021703` | Metro | empty | empty | empty |
| Dalens sjukhus buses | `740065542` | Bus | `163` | `816` | empty |

Both examples show both directions. Blåsut's stop group also includes buses, so select Metro explicitly.

## Reading the tile

- Destination identifies the direction. The next departure counts down; larger tiles list more departures.
- `+2` means two minutes late. `TT` means timetable only, without a realtime prediction.
- Walking time hides departures you cannot reach. The countdown still shows time until departure, not time to leave home.
- Canceled departures are omitted. Empty results say “No departures”; this covers the API's next 60 minutes only.
- “Old data” means the last successful response is being shown after a fetch failure. The source credit alternates this warning and the data attribution.
- The compact source credit shows Trafiklab.se in the smallest theme text size. It sits below the departures, keeping all departure times aligned. Row spacing tightens where needed to fit three departures plus the credit on Guition 1×3. The editor's simplified preview does not reproduce every screen annotation.

## Requests and limits

Tessera fetches every 60 seconds for each distinct stop URL and shares its response between tiles of this plugin.
Two stops continuously active use an estimated 89,280 departure requests in 31 days, before editor lookups and retries. Stop searches are cached for one day per query. Line dropdowns use the same departure URL and 60-second cache as the tile; opening them can fetch data when that cache is cold. Realtime Bronze currently allows 100,000 requests/month, which accommodates these two stops with some margin. More stops or other users of the same key need their own budget. This is an estimate, not an enforced account-wide cap.

The interval is currently a manifest constant. Tessera 0.4.88 has no plugin setting for runtime fetch intervals, polling schedules, or computed editor fields. See ROADMAP.md for these requested enhancements.
The plugin sends at most the next 12 filtered departures, bounded further by Tessera's message budget; very frequent services or long walking times can exhaust this window before the next refresh.
The response must fit Tessera's 64 KiB fetch limit. Busy hubs may exceed it; filtering happens after download and cannot reduce the HTTP response size.
The two example stops returned approximately 17 KB and 9 KB during initial verification, not a guarantee for every time of day.

Trafiklab returns local timestamps without UTC offsets. They are interpreted in Europe/Stockholm. During the repeated hour when daylight saving ends, an offset-free time can be ambiguous.
Realtime availability varies by operator. Missing realtime is labeled TT, not represented as a live prediction.

## Privacy

The Tessera app in Home Assistant sends the selected stop ID and API key over HTTPS to `realtime-api.trafiklab.se`.
Trafiklab sees those values and your public IP address. The key is a Tessera secret input and is never sent to the display or stored in this repository.
The plugin does not read Home Assistant entities or call Home Assistant actions.

## Data and license

Data from [Trafiklab.se](https://www.trafiklab.se/api/our-apis/trafiklab-realtime-apis/timetables/), under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The plugin filters and reformats the data into countdowns.
Trafiklab requires source attribution on screens and website widgets displaying this data; see the [Timetables attribution requirement](https://www.trafiklab.se/api/our-apis/trafiklab-realtime-apis/timetables/#license). This is why the tile retains a visible “Trafiklab.se” credit. The exact placement is our layout choice, not a requirement: the compact credit sits below the departure rows. Keep attribution when adapting the display. This README links the data source and license and explains the transformation above.

Plugin code is MIT licensed. The tile adapts Max Gramser's MIT-licensed `ov_departures`; its copyright and license are preserved in NOTICE.

## Development

Clone https://github.com/MaxGramser/tessera-plugins beside this repository and follow AGENTS.md.

```sh
python3 ../tessera-plugins/tools/preview.py --setup
python3 ../tessera-plugins/tools/check.py .
python3 ../tessera-plugins/tools/preview.py . --strict
python3 ../tessera-plugins/tools/store_image.py . --from .preview
TESSERA_TREE=../homeassistant_espscreen python3 -m unittest discover -s tests -v
```

Tests need PyYAML and aiohttp (the preview virtual environment includes them).
No API key is needed for the deterministic tests and previews. Never commit credentials or raw authenticated request URLs.
Physical hardware acceptance is separate from simulator checks; see VALIDATION.md.

## GitHub Actions

The `Plugin CI` workflow runs on pushes, pull requests and manually from the Actions tab:

- Checks the manifest against the supported Tessera API 0.10 and runs the deterministic mapper tests.
- Compiles the plugin C++ into the Guition host simulator and runs strict layout checks, including the 1×3 grid.
- Uploads preview images, logs and the report as the `guition-preview` artifact for seven days, including on a failed preview when files are available.

No Trafiklab API key or Home Assistant credentials are needed; tests use fixtures and make no Trafiklab calls.
The workflow has read-only repository permissions and does not publish releases or install firmware.
Tessera and its plugin tools are pinned to the commits recorded in the workflow; update them deliberately when changing the supported API.
A simulator build runs on Linux and is not an ESP32 firmware cross-build. Continue building the real Guition firmware in Tessera and testing it on the device.
The first hosted workflow run after pushing must still be checked in GitHub Actions; local checks do not validate the hosted runner environment.

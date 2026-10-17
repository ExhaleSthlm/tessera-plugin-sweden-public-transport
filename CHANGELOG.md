# Changelog

## 0.1.2
- Rename the plugin to Public transport (SE) in the plugin picker.
- Tessera 0.4.88 cannot clear a dynamic choice: create a new tile to return to all lines after selecting a filter.
- Select both line filters from dropdowns populated by the selected stop.
- Choices include lines in the next hour, deduplicated across directions. Existing saved line numbers are preserved; reselect them when changing stops.

## 0.1.1
- Compact data attribution shares the last departure row on wide tiles, freeing vertical space.
- Wide tiles also show departure lists in a one-column grid (including Guition 1x3).
- Rebuild and install the screen firmware to apply the layout change.

## 0.1.0
- First beta: Swedish departures from Trafiklab Timetables.
- Independent stop, two line filters, transport mode and destination per tile.
- Swedish and English texts, walking time, delays and timetable-only indication.
- Built-in stop name search and selection, with daily lookup caching.
- One-minute updates; approximately 89,280 departure calls per 31 days for two stops.

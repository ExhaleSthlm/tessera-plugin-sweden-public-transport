# Changelog

## 0.2.2
- Give the translated old-data warning the full footer width, keeping it right-aligned below the departures.
- Rebuild and install screen firmware to apply the fix; existing tile settings are unchanged.

## 0.2.1
- Replace the two line dropdowns with one removable selection of up to eight lines.
- At least one line is required; removing all selections shows Choose lines and stops departure polling for that tile.
- Filter each selected line before merging, sorting and limiting departures; responses share the same stop cache.
- Upgrade: select lines again (18 for Blåsut, 163 and 816 for Dalens sjukhus), save the layout, and rebuild/install firmware. Reselect the stop too when upgrading from 0.1.x.

## 0.2.0
- Requires Tessera 0.4.89 and firmware 0.57.0 (plugin API 0.12).
- Search for and select a stop in one control; the selected name stays visible.
- Upgrade from 0.1.x: reselect the stop in existing tiles, then rebuild and install firmware. The old scalar stop value cannot be converted automatically by the plugin. The two line fields remain unchanged in 0.2.0; their replacement follows in 0.2.1.

## 0.1.3
- Keep departure times aligned with a separate source credit below compact rows.
- Upgrade GitHub Actions to Node.js 24 versions.
- Rebuild and install the screen firmware for the layout update.

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

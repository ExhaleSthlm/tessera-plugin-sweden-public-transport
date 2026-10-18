# Follow-up design

## Available in this beta

- Integrated stop search using Trafiklab Stop Lookup and Tessera API 0.12. Searches start after a 300 ms typing pause with at least two characters; searched results are cached for ten minutes.
- One to eight selected lines with removable choices, optional transport mode and destination; empty destination shows both directions. At least one line is required.
- A fixed 60-second departure interval. For two distinct stops, a 31-day month estimates 89,280 departure calls, plus lookup traffic, retries and cache resets. Trafiklab Realtime Bronze currently documents 100,000 requests/month and 25/minute. Other clients sharing the key consume the same quota.

## Requires Tessera support or a separate Home Assistant integration

Tessera 0.4.89 parses `fetch.every` as a constant duration. It does not accept a tile-option placeholder there, a daily fetch schedule, or arbitrary computed inspector fields. A plugin cannot execute Python in the Tessera app. Merely hiding a tile at night does not guarantee that requests stop.

For adjustable polling, quiet hours and a global request estimate, prefer a general upstream Tessera enhancement. An alternative is a Home Assistant integration that owns fetching, schedules and counters; the display plugin reads its entities. That is an architectural extension, not an unsupported manifest field.

Proposed controls when supported:

- Interval in seconds, at least 60 for this API's cache duration.
- Enabled days and daily active window, explicitly in Europe/Stockholm; support windows crossing midnight.
- Distinct stop count shared across screens, monthly budget and reserved headroom.
- Estimate: distinct stops × active seconds per day ÷ interval × days in month. Label as estimated, not actual account usage.
- Actual request count and HTTP 429 handling if exposed by the backend. Track lookup calls separately.

## Authentication decision

Tessera's FETCH.md allows secrets in a header or query parameter, and prohibits them in the URL path. The current plugin uses a secret placeholder in the query, which complies with those documented rules.

Trafiklab's official OpenAPI (https://www.trafiklab.se/openapi/trafiklab-apis.yml) documents `api_key` as `name: key`, `in: query`. On 2026-10-17, read-only tests using Authorization Bearer, X-API-Key and key headers without the query returned HTTP 400. The departures endpoint reported `Missing API key` with X-API-Key.

The owner approved keeping the documented query method on 2026-10-17. The manifest contains only a secret placeholder; no credential is stored in this repository. Do not substitute an unverified header.

## Suggested later improvements

- Destination selection based on current departures, and a way to enter lines absent from the next hour.
- Platform/stop-position display and service alerts in an expanded detail view.
- Last-successful-update age and a maximum age for showing cached predictions. These need backend timestamps to avoid confusing a repeated cached state with a new fetch.
- A direction-balanced view, so frequent traffic in one direction cannot crowd out the other. Keep chronological sorting as an alternative.
- A configuration flow that clears a previous stop selection when the search is changed; the current Tessera option system does not express dependent resets.

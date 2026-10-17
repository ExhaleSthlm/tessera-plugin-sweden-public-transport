# Validation of 0.1.0

Checked on 2026-10-17.

- Tessera manifest validation against released plugin API 0.10: passed.
- Twelve deterministic tests using Tessera's real mapper: passed. Includes two bus lines in both directions, metro filtering in a mixed stop group, cancellations, stop lookup, summer/winter timestamps, ordering, payload budget and the 31-day request estimate.
- Live stop lookup and departure response mapping: verified for the two README example stops. Both response sizes were below 64 KiB. Only public transit response data was retained temporarily, without credentials.
- Host compilation and strict rendering on CYD, Guition 4-inch, Waveshare 4.3-inch portrait and Guition 10.1-inch: passed, zero layout warnings. The compiler emitted existing Tessera core warnings. The samples exercise next departure, list, timetable-only, empty and failed states in light and dark themes. Screen text previews use English; Swedish translations have matching keys and destination text includes Swedish characters.
- After adding name lookup and restoring the 60-second interval: strict Guition rendering passed again, zero layout warnings.
- Generated store.png with the upstream store-image tool and visually inspected it, plus small and large screen images.
- Credential-pattern scan: no embedded key in plugin source, documentation or test data.

Reference checkouts:

- tessera-plugins: a625674da86a6f2ba7577626407c26224ca9378c
- homeassistant_espscreen: 6943c3138e4523aff13bd1f0f1d8f0b8dab45dd0

Not yet verified:

- Physical Guition firmware build, installation, memory consumption and touch behavior.
- End-to-end stop selection in a running Tessera editor.
- User-configurable polling intervals, daily schedules and an editor quota estimate are not implemented: the current manifest does not support them.

Authentication decision: the owner approved the documented query method; the manifest uses a secret placeholder. Candidate headers returned HTTP 400 and are not used.

No firmware was uploaded and no GitHub commit, push or release was made.

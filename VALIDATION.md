# Validation of 0.1.3

- Fourteen mapper tests and API 0.10 manifest validation passed.
- Final layout rendered on all four default boards, including additional 1x3 grids: zero warnings. The preview run started before the version-only bump from 0.1.2 to 0.1.3.
- Guition 1x3 bus preview confirms three departure rows, aligned times and separate attribution below them.
- GitHub Actions now use checkout v5, setup-python v6 and upload-artifact v6; all declare Node.js 24. YAML and shell syntax checked locally; hosted CI must run after push.
- No physical firmware installation performed.

# Validation of 0.1.2

- Manifest validation against API 0.10: passed.
- Fourteen deterministic mapper tests: passed, including line-choice deduplication, sorting, independent selection and empty responses.
- Strict simulator compilation/rendering on all four default screens: passed, zero layout warnings.
- Editor source reviewed: dependent choices reload with the stop, but do not expose a clear/empty entry in Tessera 0.4.88. This limitation is documented.
- Live editor interaction and physical screen installation have not been tested for this version.

# Validation of 0.1.1

Checked on 2026-10-17.

- Manifest check against API 0.10 and all twelve mapper tests: passed.
- Strict rendering on CYD, Guition, Waveshare portrait and Guition 10.1-inch: passed, zero warnings.
- Additional Guition 1x3 grid rendering: passed, zero warnings.
- Visually checked compact source credit and three departure rows on Guition, plus small and large screen previews and the regenerated store image.
- Firmware has not been installed on the physical screen by this change.

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

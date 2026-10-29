# Product owner answer key (do NOT show to the agent up front)

Give these answers only when the agent (or gstack's /spec, /office-hours, /plan-eng-review)
asks the matching question. Copy the answer verbatim. Log every question in RESULTS_LOG.md.
This is the "human involvement" evidence for the presentation.

| Question the agent may ask | Answer |
|---|---|
| Which state has priority when several rules match? | Offline, then Charging, then Driving, then Parked. |
| Boundary: exactly at the offline timeout? | Offline only if `now - last_seen > offline_timeout_s` (strictly greater). |
| Boundary: exactly at the parked duration? | Parked when `now - zero_since >= parked_after_s` (greater or equal). |
| What counts as "last seen"? | The largest `produced_at` among readings that were applied (any signal). If `now` is earlier than last seen, treat elapsed time as 0. |
| What state before any reading? | Offline. |
| Speed is zero but not yet for the parked duration? | If the zero run started right after the vehicle was moving, stay Driving. Otherwise (never moved, or speed unknown) it is Parked. |
| Speed never reported? | Treat speed as zero starting at the produced_at of the first applied reading. |
| Charging signal true while speed above zero (electric)? | Charging wins. |
| Combustion vehicle sends the charging signal? | Accept it (it still counts as last seen) but it never affects state. |
| Unknown signal paths? | Accept, count as last seen, no other effect. |
| Late or out-of-order reading? | Applied only if `produced_at` is strictly newer than the newest applied reading for that same signal. Otherwise return `False` and change nothing, including last seen. |
| Duplicate reading (same signal, same produced_at)? | Same as late: return `False`, change nothing. |
| Invalid values? | `Vehicle.Speed` must be an int or float (not bool) and not negative, else `ValueError`. `IsCharging` must be a bool, else `ValueError`. Invalid readings change nothing. |
| Invalid profile? | `ValueError` in the constructor. |
| Return value of `update`? | `True` if the reading was applied, `False` if ignored as late or duplicate. |
| Thread safety, persistence? | Out of scope. |

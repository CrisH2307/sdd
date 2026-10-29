# Toy task: vehicle lifecycle tracker

Identical text for BOTH runs (prompt engineering and gstack). Paste it unchanged.
Language: Python 3. Test runner: pytest. No third-party runtime dependencies.

## Context

We are building a cloud digital twin of a fleet of simulated vehicles. Each vehicle
sends readings (one signal value at one time). The twin must derive a lifecycle state
for each vehicle from those readings. This task is that one component only.

## What to build

A module `lifecycle.py` with a class `LifecycleTracker` for ONE vehicle.

```python
class LifecycleTracker:
    def __init__(self, profile: str, offline_timeout_s: float = 30, parked_after_s: float = 60): ...
    def update(self, signal_path: str, value, produced_at: float) -> bool: ...
    def state(self, now: float) -> str: ...
```

- `profile` is `"electric"` or `"combustion"`.
- `update` feeds in one reading. `produced_at` and `now` are seconds on one shared clock.
- `state(now)` returns one of `"Offline"`, `"Parked"`, `"Driving"`, `"Charging"`.

## Rules (from the project charter)

| State | Entered when |
|---|---|
| Offline | No reading received from the vehicle for the configured timeout |
| Parked | Speed is zero for the configured duration and the vehicle is not charging |
| Driving | Speed is above zero |
| Charging | The charging signal is true (electric profile only) |

Signals that matter:

- `Vehicle.Speed` (km/h)
- `Vehicle.Powertrain.TractionBattery.Charging.IsCharging` (bool)

Readings for a vehicle may arrive late or out of order. A reading that arrives late must
never overwrite a newer value for the same signal.

## Deliverables

1. `lifecycle.py`
2. `test_lifecycle.py` with your own unit tests (written by you, not given to you)
3. Short README with how to run the tests

Do not ask the team for the acceptance tests. They are hidden and run after you finish.
If something is unclear, you may ask the team; answers come from the product owner.

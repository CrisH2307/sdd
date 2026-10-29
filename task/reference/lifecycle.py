"""Reference solution. Used only to prove the hidden acceptance tests are correct.
Never give this file to an agent."""

SPEED = "Vehicle.Speed"
CHARGING = "Vehicle.Powertrain.TractionBattery.Charging.IsCharging"


class LifecycleTracker:
    def __init__(self, profile: str, offline_timeout_s: float = 30, parked_after_s: float = 60):
        if profile not in ("electric", "combustion"):
            raise ValueError(f"unknown profile: {profile!r}")
        self.profile = profile
        self.offline_timeout_s = offline_timeout_s
        self.parked_after_s = parked_after_s
        self._newest = {}          # signal_path -> newest applied produced_at
        self._last_seen = None
        self._speed = None
        self._charging = False
        self._zero_since = None
        self._zero_follows_motion = False
        self._first_applied = None

    def update(self, signal_path: str, value, produced_at: float) -> bool:
        if signal_path == SPEED:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError("Vehicle.Speed must be a non-negative number")
        elif signal_path == CHARGING:
            if not isinstance(value, bool):
                raise ValueError("IsCharging must be a bool")

        prev = self._newest.get(signal_path)
        if prev is not None and produced_at <= prev:
            return False

        self._newest[signal_path] = produced_at
        if self._first_applied is None:
            self._first_applied = produced_at
        if self._last_seen is None or produced_at > self._last_seen:
            self._last_seen = produced_at

        if signal_path == SPEED:
            if value > 0:
                self._zero_since = None
            elif self._speed is None or self._speed > 0:
                self._zero_since = produced_at
                self._zero_follows_motion = self._speed is not None and self._speed > 0
            self._speed = value
        elif signal_path == CHARGING:
            self._charging = value
        return True

    def state(self, now: float) -> str:
        if self._last_seen is None:
            return "Offline"
        elapsed = max(0.0, now - self._last_seen)
        if elapsed > self.offline_timeout_s:
            return "Offline"
        if self.profile == "electric" and self._charging:
            return "Charging"
        if self._speed is not None and self._speed > 0:
            return "Driving"
        zero_since = self._zero_since if self._zero_since is not None else self._first_applied
        if now - zero_since >= self.parked_after_s:
            return "Parked"
        return "Driving" if self._zero_follows_motion else "Parked"

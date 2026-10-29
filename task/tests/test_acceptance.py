"""Hidden acceptance tests for the lifecycle toy task.

Two groups, reported separately in the results log:
  stated : behaviour written in TASK.md
  edge   : behaviour only settled by ANSWER_KEY.md (ambiguity the agent had to resolve)

Run:  pytest -q test_acceptance.py            (all)
      pytest -q -m stated test_acceptance.py
      pytest -q -m edge test_acceptance.py
Put the agent's lifecycle.py on PYTHONPATH (or next to this file).
"""
import pytest

from lifecycle import LifecycleTracker

SPEED = "Vehicle.Speed"
CHG = "Vehicle.Powertrain.TractionBattery.Charging.IsCharging"

stated = pytest.mark.stated
edge = pytest.mark.edge


def ev(**kw):
    return LifecycleTracker("electric", **kw)


def ice(**kw):
    return LifecycleTracker("combustion", **kw)


# ---------------------------------------------------------------- stated

@stated
def test_driving_when_speed_positive():
    t = ev()
    t.update(SPEED, 50, 100)
    assert t.state(101) == "Driving"


@stated
def test_parked_after_zero_speed_for_duration():
    t = ev(parked_after_s=60, offline_timeout_s=1000)
    t.update(SPEED, 0, 100)
    t.update(SPEED, 0, 130)
    assert t.state(170) == "Parked"


@stated
def test_charging_when_signal_true_electric():
    t = ev()
    t.update(SPEED, 0, 100)
    t.update(CHG, True, 101)
    assert t.state(102) == "Charging"


@stated
def test_offline_after_timeout():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    assert t.state(131) == "Offline"


@stated
def test_online_just_before_timeout():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    assert t.state(125) == "Driving"


@stated
def test_combustion_ignores_charging():
    t = ice()
    t.update(SPEED, 30, 100)
    t.update(CHG, True, 101)
    assert t.state(102) == "Driving"


@stated
def test_late_reading_does_not_overwrite_newer():
    t = ev()
    t.update(SPEED, 0, 100)
    t.update(SPEED, 40, 110)
    t.update(SPEED, 0, 105)  # late
    assert t.state(111) == "Driving"


@stated
def test_charge_stops_returns_to_other_state():
    t = ev(parked_after_s=10)
    t.update(SPEED, 0, 100)
    t.update(CHG, True, 101)
    t.update(CHG, False, 105)
    assert t.state(120) == "Parked"


@stated
def test_driving_resumes_after_parked():
    t = ev(parked_after_s=10)
    t.update(SPEED, 0, 100)
    assert t.state(115) == "Parked"
    t.update(SPEED, 25, 116)
    assert t.state(117) == "Driving"


@stated
def test_state_returns_exact_strings():
    t = ev()
    t.update(SPEED, 10, 1)
    assert t.state(2) in {"Offline", "Parked", "Driving", "Charging"}


# ---------------------------------------------------------------- edge

@edge
def test_no_readings_is_offline():
    assert ev().state(0) == "Offline"


@edge
def test_offline_boundary_is_strictly_greater():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    assert t.state(130) == "Driving"
    assert t.state(130.001) == "Offline"


@edge
def test_parked_boundary_is_greater_or_equal():
    t = ev(parked_after_s=60, offline_timeout_s=1000)
    t.update(SPEED, 20, 100)
    t.update(SPEED, 0, 110)
    t.update(SPEED, 0, 130)
    assert t.state(169.9) == "Driving"
    assert t.state(170) == "Parked"


@edge
def test_stopped_briefly_after_moving_stays_driving():
    t = ev(parked_after_s=60)
    t.update(SPEED, 20, 100)
    t.update(SPEED, 0, 110)
    assert t.state(120) == "Driving"


@edge
def test_never_moved_zero_speed_is_parked_immediately():
    t = ev(parked_after_s=60)
    t.update(SPEED, 0, 100)
    assert t.state(101) == "Parked"


@edge
def test_speed_never_reported_counts_as_zero_from_first_reading():
    t = ev(parked_after_s=60, offline_timeout_s=1000)
    t.update("Vehicle.TraveledDistance", 1000.0, 100)
    assert t.state(120) == "Parked"
    assert t.state(161) == "Parked"


@edge
def test_charging_beats_driving():
    t = ev()
    t.update(SPEED, 30, 100)
    t.update(CHG, True, 101)
    assert t.state(102) == "Charging"


@edge
def test_offline_beats_charging():
    t = ev(offline_timeout_s=30)
    t.update(CHG, True, 100)
    assert t.state(200) == "Offline"


@edge
def test_unknown_signal_counts_as_last_seen():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    t.update("Vehicle.Cabin.Door.Row1.DriverSide.IsOpen", True, 125)
    assert t.state(150) == "Driving"


@edge
def test_combustion_charging_still_counts_as_last_seen():
    t = ice(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    t.update(CHG, True, 125)
    assert t.state(150) == "Driving"


@edge
def test_update_return_values():
    t = ev()
    assert t.update(SPEED, 10, 100) is True
    assert t.update(SPEED, 20, 100) is False  # duplicate timestamp
    assert t.update(SPEED, 20, 99) is False   # late
    assert t.update(SPEED, 20, 101) is True


@edge
def test_late_reading_does_not_move_last_seen():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    t.update(CHG, False, 90)   # first reading for CHG, applied, but older than last seen
    assert t.state(131) == "Offline"


@edge
def test_late_reading_for_same_signal_ignored_entirely():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    assert t.update(SPEED, 5, 95) is False
    assert t.state(125) == "Driving"


@edge
def test_now_before_last_seen_is_not_offline():
    t = ev(offline_timeout_s=30)
    t.update(SPEED, 20, 100)
    assert t.state(50) == "Driving"


@edge
def test_negative_speed_rejected_and_changes_nothing():
    t = ev()
    t.update(SPEED, 10, 100)
    with pytest.raises(ValueError):
        t.update(SPEED, -1, 101)
    assert t.state(102) == "Driving"


@edge
def test_bool_speed_rejected():
    with pytest.raises(ValueError):
        ev().update(SPEED, True, 100)


@edge
def test_non_bool_charging_rejected():
    with pytest.raises(ValueError):
        ev().update(CHG, 1, 100)


@edge
def test_string_speed_rejected():
    with pytest.raises(ValueError):
        ev().update(SPEED, "fast", 100)


@edge
def test_invalid_profile_rejected():
    with pytest.raises(ValueError):
        LifecycleTracker("hybrid")


@edge
def test_default_parameters():
    t = LifecycleTracker("electric")
    t.update(SPEED, 0, 100)
    assert t.state(110) == "Parked"  # never moved, parked immediately
    t2 = LifecycleTracker("electric")
    t2.update(SPEED, 10, 100)
    assert t2.state(130) == "Driving"
    assert t2.state(130.5) == "Offline"

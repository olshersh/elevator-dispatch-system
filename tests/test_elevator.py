import pytest
from elevator.models import Direction, Request
from elevator.elevator import Elevator


@pytest.fixture
def elevator():
    return Elevator(id=1)


def test_initial_state(elevator):
    """Elevator should start IDLE at floor 0."""
    assert elevator.current_floor == 0
    assert elevator.direction == Direction.IDLE


def test_add_request_sets_direction(elevator):
    """Adding a request should immediately set the correct direction."""
    # Request from 5 to 10 (UP)
    req = Request(5, 10)
    elevator.add_request(req)

    assert elevator.direction == Direction.UP
    assert 5 in elevator.stops
    assert 10 in elevator.stops


def test_immediate_pickup_direction(elevator):
    """
    Edge Case: User is at floor 0 (current), wants to go to 10.
    Elevator must switch to UP immediately, not stay IDLE.
    """
    elevator.current_floor = 0
    req = Request(0, 10)  # UP request starting from HERE

    elevator.add_request(req)

    # Must adopt the request's direction
    assert elevator.direction == Direction.UP
    assert 0 in elevator.stops


def test_number_of_stops_before_direct_path(elevator):
    # Setup: Elevator moving 0 -> 10
    elevator.add_request(Request(0, 10))
    # Simulate door opening at 0 to set state to moving
    elevator.move_to_next_stop()

    # Current State: Floor 0, UP, Stops [10]
    req = Request(5, 8)
    cost = elevator.number_of_stops_before(req)

    assert cost == 0


def test_number_of_stops_before_turnaround(elevator):
    """
    Scenario: Elevator at 10, going UP to 20.
    new request 11 to 17. Move once to next stop.
    arrived to 11.
    New Request: At 5 (Behind it).
    """
    elevator.current_floor = 10
    elevator.add_request(Request(10, 20))
    elevator.add_request(Request(11, 17))

    elevator.move_to_next_stop()  # Doors open at 10

    req = Request(5, 0)  # Request at 5 (Down)
    cost = elevator.number_of_stops_before(req)

    assert cost == 2


def test_move_step_teleport(elevator):
    """
    If elevator is at 0, next stop 5.
    Step should teleport to 5.
    """
    elevator.add_request(Request(5, 10))
    # Stops: [5, 10]. Dir: UP.

    status = elevator.move_to_next_stop()

    assert elevator.current_floor == 5
    assert 5 not in elevator.stops  # 5 removed

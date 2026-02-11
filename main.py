import time
from elevator.models import Direction
from elevator.manager import ElevatorManager


def run_simulation():
    manager = ElevatorManager(num_elevators=2)

    manager.handle_request(from_floor=0, to_floor=10)
    manager.handle_request(from_floor=11, to_floor=20)

    for _ in range(3):
        manager.process()
        time.sleep(1)

    print("Add new request")
    manager.handle_request(from_floor=3, to_floor=7)
    manager.handle_request(from_floor=0, to_floor=1)

    for _ in range(5):
        manager.process()
        time.sleep(1)


if __name__ == "__main__":
    run_simulation()

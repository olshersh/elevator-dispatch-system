import queue
from typing import List
from .models import Request, Direction
from .elevator import Elevator


class ElevatorManager:

    def __init__(self, num_elevators: int):
        self.elevators = [Elevator(i) for i in range(num_elevators)]
        self.request_queue = queue.Queue()

    def find_best_elevator(self, req: Request) -> Elevator:
        return min(self.elevators, key=lambda e: e.number_of_stops_before(req))

    def handle_request(self, from_floor: int, to_floor: int):

        req = Request(from_floor, to_floor)
        best_elevator = min(self.elevators, key=lambda e: e.number_of_stops_before(req))
        best_elevator.add_request(req)
        print(
            f"Request {from_floor} --> {to_floor} assigned to Elevator {best_elevator.id}"
        )

    def process(self):
        print("-" * 30)
        for elev in self.elevators:
            status = elev.move_to_next_stop()
            if status != Direction.IDLE:
                print(f"Elevator {elev.id}: Stops: {elev.stops}")

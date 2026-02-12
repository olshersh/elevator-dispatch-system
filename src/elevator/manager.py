from typing import List
from .models import Request, Direction
from .elevator import Elevator


class ElevatorManager:

    def __init__(self, num_elevators: int):
        self.elevators = [Elevator(i) for i in range(num_elevators)]

    def find_best_elevator(self, req: Request) -> Elevator:
        """return elevator that has the minimal numbers of stops in order to pickup this request"""
        return min(self.elevators, key=lambda e: e.number_of_stops_before(req))

    def handle_request(self, from_floor: int, to_floor: int):
        """assign the request to most suitable elevator"""
        req = Request(from_floor, to_floor)
        best_elevator = min(self.elevators, key=lambda e: e.number_of_stops_before(req))
        best_elevator.add_request(req)
        print(
            f"Request {from_floor} --> {to_floor} assigned to Elevator {best_elevator.id}"
        )

    def process(self):
        """move all elevators once, to their respective next stop"""
        print("-" * 30)
        for elev in self.elevators:
            status = elev.move_to_next_stop()
            if status != Direction.IDLE:
                print(f"Elevator {elev.id}: Stops: {elev.stops}")

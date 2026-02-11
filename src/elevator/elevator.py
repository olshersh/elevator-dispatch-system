import bisect
from typing import List, Optional
from .models import Direction, Request


class Elevator:

    def __init__(self, id: int):
        self.id = id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.stops: List[int] = []

    def add_stop(self, floor: int):
        if floor not in self.stops:
            bisect.insort(self.stops, floor)

    def number_of_stops_before(self, req: Request) -> int:
        """Caclculate number of stops that will be required to arrive to req.from floor,
        by checking all the direction cases and the number of stops that this elevator already has on the
         way to req.from"""

        if not self.stops:
            return 0

        # to get the next stop index above current floor
        indx_current_right = bisect.bisect_right(self.stops, self.current_floor)

        # to get the stop below or equal the current floor
        indx_current_left = bisect.bisect_left(self.stops, self.current_floor)

        # indexes for the pickup
        indx_target_right = bisect.bisect_right(self.stops, req.from_floor)

        indx_target_left = bisect.bisect_left(self.stops, req.from_floor)

        if self.direction == req.direction:
            if self.direction == Direction.UP and req.from_floor > self.current_floor:

                return indx_target_right - indx_current_right

            if self.direction == Direction.DOWN and req.from_floor < self.current_floor:

                return indx_current_left - indx_target_left

        # turnaround
        if self.direction == Direction.UP:
            return len(self.stops) - indx_current_right

        if self.direction == Direction.DOWN:
            return indx_current_left

        return 0

    def add_request(self, req: Request):
        """Add both req.from and req.to as stops to this elevator"""
        self.add_stop(req.from_floor)
        self.add_stop(req.to_floor)
        if self.direction == Direction.IDLE:

            if req.from_floor > self.current_floor:
                self.direction = Direction.UP
            elif req.from_floor < self.current_floor:
                self.direction = Direction.DOWN
            else:
                self.direction = req.direction

    def move_to_next_stop(self):
        """the elevator moves to the next stop in the stops list"""

        if not self.stops:
            self.direction = Direction.IDLE
            return

        current_floor_indx = bisect.bisect_left(self.stops, self.current_floor)

        if (
            current_floor_indx < len(self.stops)
            and self.stops[current_floor_indx] == self.current_floor
        ):
            print(
                f" [ARRIVED] Elevator {self.id} @ Floor {self.current_floor}. Doors Opening."
            )
            self.stops.pop(current_floor_indx)
            if not self.stops:
                self.direction = Direction.IDLE
                print("Elevator {self.id} served all existing requests. Idle")
                return

        next_floor = None

        # find recursively next floor to move

        if self.direction == Direction.UP:
            # find the closest index in the stops
            closest_indx = bisect.bisect_right(self.stops, self.current_floor)
            if closest_indx < len(self.stops):
                next_floor = self.stops[closest_indx]
            else:
                self.direction = Direction.DOWN
                return self.move_to_next_stop()
        elif self.direction == Direction.DOWN:
            # find the closest index in the stops
            closest_indx = bisect.bisect_left(self.stops, self.current_floor)
            if closest_indx > 0:
                next_floor = self.stops[closest_indx - 1]
            else:
                self.direction = Direction.UP
                return self.move_to_next_stop()
        elif self.direction == Direction.IDLE:
            self.direction = (
                Direction.UP if self.stops[-1] > self.current_floor else Direction.DOWN
            )
            return self.move_to_next_stop()

        # execute the move

        if next_floor is not None:
            self.current_floor = next_floor
            current_floor_indx = bisect.bisect_left(self.stops, self.current_floor)

            if (
                current_floor_indx < len(self.stops)
                and self.stops[current_floor_indx] == self.current_floor
            ):
                print(
                    f" [ARRIVED] Elevator {self.id} @ Floor {self.current_floor}. Doors Opening."
                )
                self.stops.pop(current_floor_indx)
                if not self.stops:
                    self.direction = Direction.IDLE
                    print(f"Elevator {self.id} served all existing requests. Idle")
                    return

import enum
import random

class State(enum.Enum):
    IDLE = "idle"
    WALK_LEFT = "walk_left"
    WALK_RIGHT = "walk_right"
    EAT = "eat"
    SLEEP = "sleep"
    PETTED = "pet"
    DRAGGED = "drag"
    FALLING = "falling"


class HamsterBehavior:
    def __init__(self):
        self.state = State.IDLE
        self.state_timer = 0  # ticks in current state
        self.target_ticks = 100  # duration before next spontaneous choice
        self.walk_speed = 2.0
        self.gravity = 1.4
        self.vy = 0.0

    def set_state(self, new_state: State, duration_ticks: int = None):
        self.state = new_state
        self.state_timer = 0
        if duration_ticks is not None:
            self.target_ticks = duration_ticks
        else:
            self.target_ticks = self._get_default_duration(new_state)

    def _get_default_duration(self, state: State) -> int:
        if state == State.IDLE:
            return random.randint(90, 210)  # ~3 - 7 seconds at 30fps
        elif state in (State.WALK_LEFT, State.WALK_RIGHT):
            return random.randint(60, 180)  # ~2 - 6 seconds of walking
        elif state == State.EAT:
            return random.randint(150, 240)  # ~5 - 8 seconds of munching
        elif state == State.PETTED:
            return 75  # ~2.5 seconds
        elif state == State.SLEEP:
            return random.randint(900, 1800)  # ~30 - 60 seconds nap
        return 100

    def decide_next_state(self, can_roam=True) -> State:
        """Autonomous AI decision when idle/walk finishes"""
        if not can_roam:
            return State.IDLE

        choices = [
            (State.IDLE, 30),
            (State.WALK_LEFT, 25),
            (State.WALK_RIGHT, 25),
            (State.EAT, 15),
            (State.SLEEP, 5),
        ]
        total = sum(w for _, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for st, weight in choices:
            if upto + weight >= r:
                return st
            upto += weight
        return State.IDLE

    def update_tick(self, current_x: int, min_x: int, max_x: int, can_roam: bool = True) -> tuple[int, int, bool]:
        """
        Runs one tick (1/30s).
        Returns: (dx, dy, state_changed)
        """
        self.state_timer += 1
        dx, dy = 0, 0
        changed = False

        if self.state == State.WALK_LEFT:
            if not can_roam:
                self.set_state(State.IDLE)
                return 0, 0, True
            dx = -int(self.walk_speed)
            if current_x + dx <= min_x:
                # Reached left screen edge, turn around!
                self.set_state(State.WALK_RIGHT, random.randint(60, 150))
                return 0, 0, True

        elif self.state == State.WALK_RIGHT:
            if not can_roam:
                self.set_state(State.IDLE)
                return 0, 0, True
            dx = int(self.walk_speed)
            if current_x + dx >= max_x:
                # Reached right screen edge, turn around!
                self.set_state(State.WALK_LEFT, random.randint(60, 150))
                return 0, 0, True

        elif self.state == State.FALLING:
            self.vy += self.gravity
            dy = int(self.vy)

        # Check if state time expired (except for dragged and falling which are physics-driven)
        if self.state not in (State.DRAGGED, State.FALLING):
            if self.state_timer >= self.target_ticks:
                next_st = self.decide_next_state(can_roam)
                self.set_state(next_st)
                changed = True

        return dx, dy, changed

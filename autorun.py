from pico2d import get_time


class AutoRun:
    SPEED_GROWTH_PER_SECOND = 0.5

    def __init__(self, boy):
        self.boy = boy
        self.started_at = None
        self.timeout_reported = False

    def enter(self):
        self.boy.frame = 0
        self.boy.face_dir = -1
        self.boy.move_direction = -1
        self.started_at = get_time()
        self.timeout_reported = False

    def update(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        elapsed = max(0, get_time() - self.started_at)
        speed = self.boy.RUN_SPEED * (
            1 + elapsed * self.SPEED_GROWTH_PER_SECOND
        )
        next_x = self.boy.x + self.boy.move_direction * speed
        if self.boy.move_direction < 0 and next_x <= self.boy.MIN_X:
            print("hello")
            self.boy.x = self.boy.MIN_X
            self.boy.move_direction = 1
            self.boy.face_dir = 1
        elif self.boy.move_direction > 0 and next_x >= self.boy.MAX_X:
            print("hello")
            self.boy.x = self.boy.MAX_X
            self.boy.move_direction = -1
            self.boy.face_dir = -1
        else:
            self.boy.x = next_x
        just_timed_out = False
        if (
            not self.timeout_reported
            and elapsed >= 5
        ):
            print("hello")
            self.timeout_reported = True
            just_timed_out = True
        return just_timed_out

    def draw(self):
        self.boy.image.clip_draw(
            self.boy.frame * 100,
            100 if self.boy.face_dir == 1 else 0,
            100,
            100,
            self.boy.x,
            self.boy.y,
        )

class AutoRun:
    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0
        self.boy.face_dir = -1
        self.boy.move_direction = -1

    def update(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x = max(
            self.boy.x - self.boy.RUN_SPEED,
            self.boy.MIN_X,
        )

    def draw(self):
        self.boy.image.clip_draw(
            self.boy.frame * 100,
            0,
            100,
            100,
            self.boy.x,
            self.boy.y,
        )

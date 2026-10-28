from pico2d import *
import math

from transitions import Machine


class AutoRun:
    def enter(self):
        print("hello")

    def update(self):
        pass


class Boy:
    MIN_X = 50
    MAX_X = 750
    RUN_SPEED = 10

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.move_direction = 0
        self.idle_started_at = get_time()
        self.auto_run = AutoRun()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=[
                {'name': 'IDLE', 'on_enter': 'start_idle_timer'},
                {'name': 'SLEEP', 'on_enter': 'start_sleep'},
                {'name': 'RUN', 'on_enter': 'start_run'},
                {'name': 'AUTO_RUN', 'on_enter': 'on_enter_auto_run'},
            ],
            transitions=[
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'begin_run', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'end_run', 'source': 'RUN', 'dest': 'IDLE'},
                {'trigger': 'begin_auto_run', 'source': 'IDLE', 'dest': 'AUTO_RUN'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if get_time() - self.idle_started_at >= 5:
                self.fall_asleep()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x = min(
                max(self.x + self.move_direction * self.RUN_SPEED, self.MIN_X),
                self.MAX_X,
            )
        elif self.state == 'AUTO_RUN':
            self.auto_run.update()

    def start_idle_timer(self):
        self.idle_started_at = get_time()

    def on_enter_auto_run(self):
        self.auto_run.enter()

    def start_auto_run(self):
        if self.state == 'IDLE':
            self.begin_auto_run()

    def start_sleep(self):
        self.frame = 0

    def start_run(self):
        self.frame = 0

    def handle_space(self):
        if self.state == 'SLEEP':
            self.wake_up()

    def start_running(self, direction):
        self.move_direction = direction
        self.face_dir = direction
        if self.state != 'RUN':
            self.begin_run()

    def stop_running(self):
        if self.state == 'RUN':
            self.move_direction = 0
            self.end_run()

    def draw(self):
        if self.state == 'RUN':
            source_y = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(
                self.frame * 100, source_y, 100, 100, self.x, self.y,
            )
            return

        source_y = 300 if self.face_dir == 1 else 200
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(
                self.frame * 100, source_y, 100, 100,
                math.pi / 2, '', self.x, self.y - 17, 100, 100,
            )
            return

        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)

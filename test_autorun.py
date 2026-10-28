import contextlib
import io
import unittest

import autorun
import boy


class AutoRunKeyboardTests(unittest.TestCase):
    def setUp(self):
        self.clock = [0.0]
        boy.get_time = lambda: self.clock[0]
        autorun.get_time = lambda: self.clock[0]
        boy.load_image = lambda _name: object()
        self.boy = boy.Boy()
        self.boy.start_auto_run()

    def test_a_key_starts_auto_run_from_sleep(self):
        self.boy.end_auto_run()
        self.boy.fall_asleep()

        self.boy.start_auto_run()

        self.assertEqual(self.boy.state, 'AUTO_RUN')
        self.assertEqual(self.boy.move_direction, -1)
        self.assertEqual(self.boy.face_dir, -1)

    def test_left_key_runs_left_and_returns_to_idle_when_released(self):
        self.boy.start_running(-1)

        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.move_direction, -1)
        self.assertEqual(self.boy.face_dir, -1)

        start_x = self.boy.x
        self.boy.update()
        self.assertEqual(self.boy.x, start_x - self.boy.RUN_SPEED)

        self.boy.stop_running()
        self.assertEqual(self.boy.state, 'IDLE')

    def test_left_key_overrides_auto_run_direction_after_right_wall(self):
        self.boy.x = self.boy.MAX_X - self.boy.RUN_SPEED
        self.boy.move_direction = 1
        self.boy.face_dir = 1
        with contextlib.redirect_stdout(io.StringIO()):
            self.boy.auto_run.update()
        self.assertEqual(self.boy.move_direction, -1)

        self.boy.start_running(-1)
        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.move_direction, -1)

    def test_right_key_runs_right_and_returns_to_idle_when_released(self):
        self.boy.start_running(1)

        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.move_direction, 1)
        self.assertEqual(self.boy.face_dir, 1)

        start_x = self.boy.x
        self.boy.update()
        self.assertEqual(self.boy.x, start_x + self.boy.RUN_SPEED)

        self.boy.stop_running()
        self.assertEqual(self.boy.state, 'IDLE')

    def test_right_key_overrides_auto_run_direction_after_left_wall(self):
        self.boy.x = self.boy.MIN_X + self.boy.RUN_SPEED
        self.boy.move_direction = -1
        self.boy.face_dir = -1
        with contextlib.redirect_stdout(io.StringIO()):
            self.boy.auto_run.update()
        self.assertEqual(self.boy.move_direction, 1)

        self.boy.start_running(1)
        self.assertEqual(self.boy.state, 'RUN')
        self.assertEqual(self.boy.move_direction, 1)
        self.assertEqual(self.boy.face_dir, 1)


if __name__ == '__main__':
    unittest.main()

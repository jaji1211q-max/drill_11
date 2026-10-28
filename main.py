from pico2d import *
from boy import Boy
from grass import Grass


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            stop_game()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                stop_game()
            elif event.key == SDLK_SPACE:
                boy.handle_space()
            elif event.key == SDLK_a:
                boy.start_auto_run()
            elif event.key == SDLK_LEFT:
                movement_keys.add(event.key)
                boy.start_running(-1)
            elif event.key == SDLK_RIGHT:
                movement_keys.add(event.key)
                boy.start_running(1)
        elif event.type == SDL_KEYUP and event.key in movement_keys:
            movement_keys.remove(event.key)
            if movement_keys:
                direction = -1 if SDLK_LEFT in movement_keys else 1
                boy.start_running(direction)
            else:
                boy.stop_running()


def stop_game():
    global running
    running = False


def reset_world():
    global world
    global boy

    world = []
    movement_keys.clear()

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True
movement_keys = set()

open_canvas()
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()

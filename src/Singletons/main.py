# from pico2d import *
# from pico2d import get_time
# from sdl2 import SDL_KEYDOWN, SDLK_a, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP
# from math import pi
#
#
# #push test 2
#
# WIDTH,HEIGHT = 800,600
# class Boy:
#     event = None
#     def __init__(self):
#         self.x, self.y = 400, 90
#         self.state_machine = None
#         self.speed = 300
#         self.sizeX,self.sizeY = 100,100
#     def update(self):
#         self.state_machine.update(Boy.event)
#     def draw(self):
#         self.state_machine.render()
# class State:
#     def __init__(self,state_machine):
#         self.state_machine = state_machine
#         self.event_for_check = None
#         self.frame = 0
#     def enter_state(self):
#         pass
#     def exit_state(self):
#         pass
#     def update(self):
#         pass
#     def render(self):
#         pass
#     def change_state(self,event):
#         pass
#
# class Idle(State):
#     def __init__(self,state_machine):
#         super().__init__(state_machine)
#         self.startTime = get_time()
#     def enter_state(self):
#         self.frame = 0
#         self.startTime = get_time()
#     def exit_state(self):
#         pass
#     def update(self):
#         if get_time() - self.startTime >= 5:
#             self.state_machine.change_idle_to_sleep()
#     def render(self):
#         dir = '' if self.state_machine.boy_dir == 1 else 'h'
#         boy = self.state_machine.boy
#         self.state_machine.boy_anim.clip_composite_draw(self.frame * 100, 300, 100, 100,
#                             0, dir, boy.x, boy.y,
#                             boy.sizeX, boy.sizeY)
#         self.frame = (self.frame + 1) % 8
#     def change_state(self,event):
#         if get_time() - self.startTime >= 5:
#             return 'Sleep'
#         if event.type == SDL_KEYDOWN:
#             if event.key == SDLK_a:
#                 return 'AutoRun'
#             if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
#                 return 'Run'
#         return ''
#
# class Run(State):
#     def __init__(self,state_machine):
#         super().__init__(state_machine)
#     def enter_state(self):
#         pass
#     def exit_state(self):
#         pass
#     def update(self):
#         self.state_machine.boy.x += self.state_machine.boy_dir * self.state_machine.boy.speed * 0.01
#     def render(self):
#         dir = '' if self.state_machine.boy_dir == 1 else 'h'
#         boy = self.state_machine.boy
#         self.state_machine.boy_anim.clip_composite_draw(self.frame * 100, 100, 100, 100,
#                                                         0, dir, boy.x, boy.y,
#                                                         boy.sizeX, boy.sizeY)
#         self.frame = (self.frame + 1) % 8
#     def change_state(self,event):
#         if event.type == SDL_KEYUP:
#             if event.key == SDLK_RIGHT and self.state_machine.boy_dir == 1:
#                 return 'Idle'
#             if event.key == SDLK_LEFT and self.state_machine.boy_dir == -1:
#                 return 'Idle'
#         return ''
#
# class StateMachine:
#     def __init__(self,boy):
#         self.cur_state = Idle(self)
#         self.boy = boy
#         self.boy_dir = 1
#         from pico2d import load_image
#         self.boy_anim = load_image('knuckles_sprite_sheet__kicks__by_alexlproductions_deidd03.png')
#         self.anim_map = {
#             "Idle" : Idle(self),
#             "Run" : Run(self),
#         }
#     def init(self):
#         self.cur_state.enter_state()
#     def update(self,event):
#         if event == None:
#             return
#         if event.type == SDL_KEYDOWN:
#             if event.key == SDLK_LEFT:
#                 self.boy_dir = -1
#             elif event.key == SDLK_RIGHT:
#                 self.boy_dir = 1
#         self.cur_state.update()
#         self.cur_state.event_for_check = event
#     def render(self):
#         self.cur_state.render()
#         self.change_state(Boy.event)
#     def change_state(self,event):
#         state = self.cur_state.change_state(event)
#         if '' != state:
#             self.cur_state.exit_state()
#             self.cur_state = self.anim_map[state]
#             self.cur_state .enter_state()
#
# ball_x,ball_y = 100+21 , 100-21
#
# def move_ball():
#     global ball_x,ball_y
#     if mon_die:
#         return
#     ball_x += 0.01 * 100 * 20
#     ball_y += 0.01 * 50 * 10
#     if ball_x >= 800 - 21 :
#         ball_x,ball_y = 100+21,100-21
# stop = False
# mon_frame = 0
# mon_die = False
# frame = 0
# def collision():
#     global mon_die
#     if ball_x >= 500-21 and ball_y >= 200-21:
#         mon_die = True
# def resume():
#     global mon_die,mon_frame,stop,ball_x,ball_y,frame
#     for eve in get_events():
#         if eve.type == SDL_KEYDOWN:
#             if eve.key == SDLK_SPACE:
#                 frame = 0
#                 mon_die = False
#                 mon_frame = 0
#                 stop = False
#                 ball_x,ball_y = 100+21,100-21
# if __name__ == '__main__':
#     open_canvas()
#     mon_anim = [None for _ in range(4)]
#     mon_anim[0] = load_image('4.png')
#     mon_anim[1] = load_image('5.png')
#     mon_anim[2] = load_image('6.png')
#     mon_anim[3] = load_image('9.png')
#     kick_img = load_image('knuckles_sprite_sheet__kicks__by_alexlproductions_deidd03.png')
#     ball = load_image('ball21x21.png')
#     while True:
#         resume()
#         move_ball()
#         kick_img.clip_draw(
#             52 * frame,
#             675 - 50 * 4,
#             50,
#             50,
#             100,
#             100,
#             100,
#             100
#         )
#         collision()
#         if mon_frame <= 3:
#             mon_anim[mon_frame].draw(500,200)
#             if mon_die:
#                 mon_frame = (mon_frame + 1)
#         ball.draw(ball_x,ball_y)
#         if not stop:
#             frame = (frame + 1) % 7
#         if frame == 0:
#             stop = True
#         update_canvas()
#         clear_canvas()
#         delay(0.04)
#
#     close_canvas()
from src.Singletons.core import CCore

CCore().Initialize(1400,700)
CCore().GameLoop()
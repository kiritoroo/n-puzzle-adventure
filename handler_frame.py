import frame_menu
import frame_game
import frame_simulator
import frame_compare

class HandlerFrame:
    def __init__(self, _screen):
        self.screen = _screen
        self.current_frame = frame_menu.Frame(self, self.screen)

    def set_current_frame(self, _str):
        if _str == 'frame_menu':
            self.current_frame = frame_menu.Frame(self, self.screen)
        elif _str == 'frame_game':
            self.current_frame = frame_game.Frame(self, self.screen)
        elif _str == 'frame_simulator':
            self.current_frame = frame_simulator.Frame(self, self.screen)
        elif _str == 'frame_compare':
            self.current_frame = frame_compare.Frame(self, self.screen)
        else:
            return
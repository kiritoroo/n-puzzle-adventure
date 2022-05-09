import frame_menu
import frame_game
import frame_simulator
import frame_compare

class HandlerFrame:
    def __init__(self):
        self.current_frame = frame_menu.Frame(self)

    def set_current_frame(self, _str):
        if _str == 'frame_menu':
            self.current_frame = frame_menu.Frame(self)
        elif _str == 'frame_game':
            self.current_frame = frame_game.Frame(self)
        elif _str == 'frame_simulator':
            self.current_frame = frame_simulator.Frame(self)
        elif _str == 'frame_compare':
            self.current_frame = frame_compare.Frame(self)
        else:
            return
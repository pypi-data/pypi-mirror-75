from collections import deque
from pyprobar.compose import *
import time
from pyprobar import probar

class Bar:

    def __init__(self, total_steps,
                 time_interval=0.02,
                 symbol_1="█", symbol_2='>',
                 color='const_random',
                 text=' ',
                 terminal=True):

        self.total_steps = total_steps
        self.q = deque(maxlen=1)
        self.q.append((1,''))

        self.__threadbar = _Thread_bar(self.q, total_steps,time_interval,
                                       symbol_1, symbol_2,
                                       color,
                                       text,
                                       terminal,
                                       time.time())
        self.__threadbar.setDaemon(True)
        self.__threadbar.start()
        self.isInterrupt = True

    def __call__(self, idx, text):
        _idx = idx + 1
        self.q.append((_idx, text))
        if _idx == self.total_steps:
            self.__threadbar.join()
            self.isInterrupt = False

N = 5000000

bar = Bar(N)
for i in range(N):
    bar(i, text=f"{i}")





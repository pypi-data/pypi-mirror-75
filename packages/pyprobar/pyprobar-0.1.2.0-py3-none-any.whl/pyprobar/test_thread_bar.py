import sys
import time
import threading
from threading import Thread
from queue import Queue
from functools import wraps
from multiprocessing import Process
from multiprocessing import Pool

import random

def d_time(d_t, t0=[]):
    """
    The unit of dt is seconds.
    Returns 1 when current time in `d_t` duration
    Returns 0 when current time out duration
    """
    if not t0:
        t0.append(time.time())
    t1 = time.time()
    if t1 - t0[0] < d_t:
        return True
    else:
        return False






class ThreadBar(Thread):
    def __init__(self, queue, N, time_interval):
        super().__init__()
        self.queue = queue
        self.stop = False
        self.N = N
        self.time_interval = time_interval

    def run(self):
        while not self.stop:
            item = self.queue.pop()
            print(item)
            time.sleep(self.time_interval)
            if item == self.N-1:
                self.stop = True

from collections import deque
# N = 1000000
# q = Queue(2)
# q = deque(maxlen=2)
# threadbar = ThreadBar(q, N, 0.1)
# threadbar.start()
# def put_queue(q):
#     q.append(i)
#
# #
# for i in range(N):
#     put_queue(q)


deq = deque(maxlen=3)
for i in range(10):
    deq.append(i)
    deq.append(i+1)
    deq.append(i + 2)
    print(deq.pop(), deq)





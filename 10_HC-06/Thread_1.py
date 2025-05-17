import _thread
import time

def th_func(delay, id):
    while True:
        time.sleep(delay)
        print('Running thread %d' % id)


_thread.start_new_thread(th_func, (1, 1))
_thread.start_new_thread(th_func, (2, 2))
_thread.start_new_thread(th_func, (3, 3))
_thread.start_new_thread(th_func, (2, 4))
_thread.start_new_thread(th_func, (1, 5))

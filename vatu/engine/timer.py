import sched
import time


def timer(callback, duration=60, interval=5):
    """ Calls *callback* every *interval* seconds during *duration* seconds
    """
    scheduler = sched.scheduler(time.time, time.sleep)
    remaining = duration
    while remaining > 0:
        scheduler.enter(remaining, 0, callback)
        remaining -= interval
    scheduler.run()

import asyncio
try:
    from asyncio import get_running_loop
except ImportError:  # pragma: no cover
    from asyncio import get_event_loop as get_running_loop  # noqa

import threading

MAX_FILENO = 60


class SelectorThread(threading.Thread):
    """ Thread with a running selector event loop """

    def __init__(self, condition):
        super().__init__(daemon=True)
        self.condition = condition
        self.num = 1

    def run(self):
        self.loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(self.loop)
        with self.condition:
            # notify pool we're ready
            self.condition.notify()
        self.loop.run_forever()

    def decrement(self):
        self.num -= 1


class SelectorPool():

    def __init__(self):
        self.threads = []

    def get_thread(self):
        for thread in self.threads:
            if thread.num < MAX_FILENO:
                thread.num += 1
                return thread

        # no available thread, create one
        condition = threading.Condition()
        with condition:
            thread = SelectorThread(condition)
            thread.start()
            # wait until loop is set up
            condition.wait()
        self.threads.append(thread)
        return thread


selector_pool = SelectorPool()

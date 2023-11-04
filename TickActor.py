import pykka


class TickActor(pykka.ThreadingActor):
    def __init__(self, config):
        super(TickActor, self).__init__()

        self._config = config

        self._sleepSeconds = config.getfloat('DEFAULT', 'sleepSeconds',
                                             fallback=0.5)
        self._intervalSeconds = config.getint('TickActor', 'intervalSeconds',
                                              fallback=2)
        self._intervalCounter = config.getint('TickActor', 'intervalCounter',
                                              fallback=0)

    def tick(self):
        self._intervalCounter += 1
        if self._intervalSeconds / self._sleepSeconds <= self._intervalCounter:
            try:
                self.doTick()
            finally:
                self._intervalCounter = 0

    def doTick(self):
        pass

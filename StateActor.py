import json
import logging

from TickActor import TickActor


class StateActor(TickActor):
    def __init__(self, config, mpdActor):
        super(StateActor, self).__init__(config)

        self._config = config
        self._mpdActor = mpdActor

        self._stateFilePath = config.get('StateActor', 'stateFilePath',
                                     fallback='data/state.json')

    def doTick(self):

        current = self._mpdActor.getCurrentSong().get()
        if current is None:
            return

        state = self.loadState()
        state["current"] = current
        try:
            state["played"][current["name"]] = current["elapsed"]
        except KeyError:
            state["played"] = {}
            state["played"][current["name"]] = current["elapsed"]

        self.saveState(state)

    def playFromLastState(self, name, fromStart=False):
        if name == self.getCurrent():
            fromStart = True

        elapsed = 0
        if not fromStart:
            elapsed = self.getElapsed(name)

        self._mpdActor.playByNameFrom(name, elapsed)

    def playLast(self, relativeElapsed=0):
        name = self.getCurrent()
        if name is not None:
            elapsed = self.getElapsed(name) + relativeElapsed
            if elapsed < 0:
                elapsed = 0

            self._mpdActor.playByNameFrom(name, elapsed)

    def getCurrent(self):
        state = self.loadState()
        try:
            return state["current"]["name"]
        except KeyError:
            logging.getLogger('sabp').info(
                'No info of currently played file. Probably a fresh start.')
            return None

    def getElapsed(self, name):
        state = self.loadState()
        try:
            return state["played"][name]
        except KeyError:
            logging.getLogger('sabp').info(
                'No info of elapsed seconds of file %s. Playing from start.' %
                name)
            return 0

    def loadState(self):
        try:
            with open(self._stateFilePath, 'r') as stateFile:
                return json.load(stateFile)
        except (IOError, ValueError) as e:
            return {}

    def saveState(self, state):
        with open(self._stateFilePath, 'w') as stateFile:
            json.dump(state, stateFile)

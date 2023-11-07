import logging
from mpd import MPDClient, CommandError
import pykka


class MpdActor(pykka.ThreadingActor):
    def __init__(self, config):
        super(MpdActor, self).__init__()
        self._config = config

        self._client = MPDClient()
        self._client.timeout = self._config.getint('MpdActor', 'timeout',
                                                 fallback=10)
        self._client.idletimeout = None

        host = self._config.get('MpdActor', 'host', fallback='localhost')
        port = self._config.getint('MpdActor', 'port', fallback=6600)
        self._client.connect(host, port)

    def getCurrentSong(self):
        try:
            name = self._client.currentsong()["file"]
            elapsed = int(float(self._client.status()["elapsed"]))

            return {"name": name, "elapsed": elapsed}
        except KeyError:
            return None

    def getCurrentState(self):
        try:
            return self._client.status()["state"]
        except KeyError:
            return None

    def playByNameFrom(self, name, playFrom):
        try:
            self._client.setvol(0)

            self._client.clear()
            self._client.add(name)
            self._client.play()

            currentSong = self._client.currentsong()
            if playFrom + 20 > int(currentSong['time']):
                # play from start, if trying to play too close from the end
                playFrom = 0

            logging.getLogger('sabp').info('Playing %s from %s' %
                                           (name, playFrom))
            self._client.seekid(currentSong['id'], playFrom)

            defaultVolume = self._config.getint('MpdActor', 'defaultVolume',
                                               fallback=100)
            self._client.setvol(defaultVolume)

        except CommandError as e:
            logging.getLogger('sabp').error('MPD Command error')
            logging.getLogger('sabp').exception(e)

    def pause(self):
        self._client.pause()

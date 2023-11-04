import configparser
import logging
from mpd import MPDClient, CommandError
import pykka


class MpdActor(pykka.ThreadingActor):
    def __init__(self, config):
        super(MpdActor, self).__init__()
        self.config = config

        self.client = MPDClient()
        self.client.timeout = self.config.getint('MpdActor', 'timeout',
                                                 fallback=10)
        self.client.idletimeout = None

        host = self.config.get('MpdActor', 'host', fallback='localhost')
        port = self.config.getint('MpdActor', 'port', fallback=6600)
        self.client.connect(host, port)

    def getCurrentSong(self):
        try:
            name = self.client.currentsong()["file"]
            elapsed = int(float(self.client.status()["elapsed"]))

            return {"name": name, "elapsed": elapsed}
        except KeyError:
            return None

    def playByNameFrom(self, name, playFrom):
        try:
            self.client.setvol(0)

            self.client.clear()
            self.client.add(name)
            self.client.play()

            currentSong = self.client.currentsong()
            if playFrom + 20 > int(currentSong['time']):
                # play from start, if trying to play too close from the end
                playFrom = 0

            logging.getLogger('sabp').info('Playing %s from %s' %
                                           (name, playFrom))
            self.client.seekid(currentSong['id'], playFrom)

            defaultVolume = self.config.getint('MpdActor', 'defaultVolume',
                                               fallback=100)
            self.client.setvol(defaultVolume)

        except CommandError as e:
            logging.getLogger('sabp').error('MPD Command error')
            logging.getLogger('sabp').exception(e)

    def pause(self):
        self.client.pause()

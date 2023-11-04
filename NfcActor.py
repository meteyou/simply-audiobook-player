import logging
from mfrc522 import SimpleMFRC522
from TickActor import TickActor


class NfcActor(TickActor):
    def __init__(self, config, tagActor):
        super(NfcActor, self).__init__(config)

        self._config = config
        self._tagActor = tagActor
        self._reader = SimpleMFRC522()

        self._currentTag = None
        self._longPressInSeconds = config.getfloat('DEFAULT',
                                                   'longPressInSeconds',
                                                   fallback=5)

    def doTick(self):
        tag = self.getTag()
        if tag is not self._currentTag:
            logging.getLogger('sabp').info('RFID read %s.' % tag)
            self._currentTag = tag
            if tag is not None:
                self.doAction(tag)

    def doAction(self, tag):
        logging.getLogger('sabp').info(
            'Calling tagActor.playByTag() with tag: %s' % tag)
        self._tagActor.playByTag(tag)

    def getCurrentTag(self):
        return self._currentTag

    def getTag(self):
        id, text = self._reader.read()

        return text

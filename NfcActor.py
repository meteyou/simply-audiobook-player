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

        # set new tag, if it is different from the current one
        if tag != self._currentTag:
            logging.getLogger('sabp').info('RFID read %s.' % tag)
            self._currentTag = tag
            if tag is not None:
                self._doAction(tag)

    def _doAction(self, tag):
        logging.getLogger('sabp').info(
            'Calling tagActor.playByTag() with tag: %s' % tag)
        self._tagActor.playByTag(tag)

    def getCurrentTag(self):
        return self._currentTag

    def getTag(self):
        try:
            id = self._reader.read_id_no_block()
            return str(id)
        except Exception as e:
            logging.getLogger('sabp').error('Error reading RFID tag.')
            logging.getLogger('sabp').exception(e)
            return None

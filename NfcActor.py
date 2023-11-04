import logging
import re
from subprocess import Popen, PIPE
from TickActor import TickActor


class NfcActor(TickActor):
    def __init__(self, config, tagActor):
        super(NfcActor, self).__init__(config)

        self._config = config
        self._tagActor = tagActor

        self._currentTag = None
        self._longPressInSeconds = config.getfloat('DEFAULT',
                                                   'longPressInSeconds',
                                                   fallback=5)

    def doTick(self):
        tag = self.getTag()
        if tag is not self._currentTag:
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
        p = Popen("nfc-list", shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        for line in out.decode("utf-8").split("\n"):
            m = re.match(r"[\s]*UID \(NFCID1\): ([a-z0-9 ]+)\b", line)
            if m:
                return m.group(1).replace(" ", "")

        return None

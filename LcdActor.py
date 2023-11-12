from RPLCD.i2c import CharLCD
from TickActor import TickActor


class LcdActor(TickActor):
    def __init__(self, config, MpdActor):
        super(LcdActor, self).__init__(config)

        self._config = config
        self._MpdActor = MpdActor
        self._lcd = CharLCD('PCF8574', 0x27, auto_linebreaks=False)
        self._lcd.clear()

        self._lastState = None
        self._lastSong = None
        self._textPosition = 0

    def doTick(self):
        state = self._MpdActor.getCurrentState().get()
        song = self._MpdActor.getCurrentSong().get()

        if state is not None or song is not None:
            self._lcd.clear()

        if state is not None:
            self._lcd.cursor_pos = (0, 0)
            self._lcd.write_string(state.capitalize())

        if state == 'play':
            duration = int(song['duration'] / 60)
            elapsed = int(song['elapsed'] / 60)
            text = '%s/%s' % (elapsed, duration)
            textLength = len(text)
            self._lcd.cursor_pos = (0, 16 - textLength)
            self._lcd.write_string(text)

        if song is not None:
            self._textPosition += 1

            namesplits = [song['name'][i:i + 16] for i in
                          range(0, len(song['name']), 16)]
            if self._textPosition >= len(namesplits):
                self._textPosition = 0

            self._lcd.cursor_pos = (1, 0)
            self._lcd.write_string(namesplits[self._textPosition])
            self._lastSong = song['name']
        else:
            self._lastSong = None

        self._lastState = state

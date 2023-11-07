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

    def doTick(self):
        state = self._MpdActor.getCurrentState().get()
        song = self._MpdActor.getCurrentSong().get()

        if (song is not None and song['name'] == self._lastSong and
                state == self._lastState):
            return

        if state is not None:
            if state == 'play':
                self._lcd.clear()
                self._lcd.write_string('Playing')
            elif state == 'pause':
                self._lcd.clear()
                self._lcd.write_string('Paused')
            elif state == 'stop':
                self._lcd.clear()
                self._lcd.write_string('Stopped')

        if song is not None:
            self._lcd.cursor_pos = (1, 0)
            self._lcd.write_string(song['name'])
            self._lastSong = song['name']
        else:
            self._lastSong = None

        self._lastState = state

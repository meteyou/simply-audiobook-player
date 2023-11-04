from time import sleep

import configparser
import logging
import pykka
import RPi.GPIO as GPIO
import signal

from MpdActor import MpdActor
from NfcActor import NfcActor
from StateActor import StateActor
from TagActor import TagActor
from WebActor import WebActor

config = configparser.ConfigParser()
config.read('simply-audiobook-player.ini')

sleepSeconds = config.getfloat('DEFAULT', 'sleepSeconds', fallback=0.5)
rewindSecondsWhenResuming = config.getfloat('DEFAULT',
                                            'rewindSecondsWhenResuming',
                                            fallback=-5 * 60)
pleaseContinue = config.getboolean('DEFAULT', 'pleaseContinue', fallback=True)
logfile = config.get('DEFAULT', 'logfile',
                     fallback='simply-audiobook-player.log')


def quitGracefully(*args):
    global pleaseContinue
    logging.getLogger('sabp').info('Received SIGINT.')
    pleaseContinue = False


def run():
    global pleaseContinue
    signal.signal(signal.SIGINT, quitGracefully)

    logging.basicConfig(filename=logfile,
                        format="%(asctime)s [%(module)s.%(funcName)s] %("
                               "levelname)s: %(message)s")
    logging.getLogger('pykka').setLevel(logging.DEBUG)
    logging.getLogger('sabp').setLevel(logging.DEBUG)

    mpdActor = MpdActor.start(config).proxy()
    stateActor = StateActor.start(config, mpdActor).proxy()

    tagActor = TagActor.start(config, stateActor).proxy()

    webActor = WebActor.start(config, tagActor).proxy()
    webActor.startServer()
    nfcActor = NfcActor.start(config, tagActor).proxy()

    stateActor.playLast(rewindSecondsWhenResuming)

    try:
        while pleaseContinue:
            stateActor.tick()
            nfcActor.tick()

            sleep(sleepSeconds)
    except KeyboardInterrupt:
        logging.getLogger('sabp').info('Received KeyboardInterrupt.')

    logging.getLogger('sabp').info('Stopping...')

    GPIO.cleanup()
    mpdActor.pause()
    pykka.ActorRegistry.stop_all()


if __name__ == "__main__":
    run()

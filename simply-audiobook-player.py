import pykka, logging, signal

from time import sleep

from WebActor import WebActor
from MpdActor import MpdActor
from StateActor import StateActor
from TagActor import TagActor
from NfcActor import NfcActor

sleepSeconds = 0.5
rewindSecondsWhenResuming = -5 * 60
pleaseContinue = True


def quitGracefully(*args):
    global pleaseContinue
    logging.getLogger('sabp').info('Received SIGINT.')
    pleaseContinue = False


def run():
    global pleaseContinue
    signal.signal(signal.SIGINT, quitGracefully)

    logging.basicConfig(filename='simply-audiobook-player.log',
                        format="%(asctime)s [%(module)s.%(funcName)s] %(levelname)s: %(message)s")
    logging.getLogger('pykka').setLevel(logging.DEBUG)
    logging.getLogger('sabp').setLevel(logging.DEBUG)

    mpdActor = MpdActor.start().proxy()
    stateActor = StateActor.start(mpdActor, sleepSeconds).proxy()

    tagActor = TagActor.start(stateActor).proxy()

    webActor = WebActor.start(tagActor).proxy()
    nfcActor = NfcActor.start(tagActor, sleepSeconds).proxy()

    stateActor.playLast(rewindSecondsWhenResuming)

    try:
        while pleaseContinue:
            stateActor.tick()
            nfcActor.tick()

            sleep(sleepSeconds)
    except KeyboardInterrupt:
        logging.getLogger('sabp').info('Received KeyboardInterrupt.')

    logging.getLogger('sabp').info('Stopping...')

    mpdActor.pause()
    pykka.ActorRegistry.stop_all()


if __name__ == "__main__":
    run()

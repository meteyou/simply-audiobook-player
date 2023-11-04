from subprocess import Popen, PIPE
import os
import pykka
import re
import shutil
from bottle import Bottle, template, redirect

# size formatting from https://stackoverflow.com/a/1094933/1166086
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


class WebActor(pykka.ThreadingActor):
    def __init__(self, config, tagActor):
        super(WebActor, self).__init__()

        self._config = config
        self._tagActor = tagActor
        self._host = config.get('WebActor', 'host', fallback='0.0.0.0')
        self._port = config.getint('WebActor', 'port', fallback=8080)
        self._fileDirPath = config.get('WebActor', 'fileDirPath',
                                       fallback='/var/lib/mpd/music/')
        self._app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', callback=self._index)
        self._app.route('/add/<name>', callback=self._add)
        self._app.route('/remove/<tag>', callback=self._remove)
        self._app.route('/play/<tag>', callback=self._play)
        self._app.route('/play/<tag>/fromStart',
                        callback=self._play_from_start)

    def startServer(self):
        self._app.run(host=self._host, port=self._port)

    def _index(self):
        total, used, free = shutil.disk_usage(self._fileDirPath)
        return template('index',
                        items=self._getItems(),
                        totalSpace=sizeof_fmt(total),
                        freeSpace=sizeof_fmt(free))

    def _add(self, name):
        self._tagActor.addTag(name).get()
        redirect('/')

    def _remove(self, tag):
        self._tagActor.removeTag(tag).get()
        redirect('/')

    def _play(self, tag):
        self._tagActor.playByTag(tag)
        return 'Called tagActor with tag: %s\n' % tag

    def _play_from_start(self, tag):
        self._tagActor.playByTag(tag, fromStart=True)
        return 'Called tagActor with tag: %s and fromStart=True\n' % tag

    def _getItems(self, **k):
        currentFiles = sorted(os.listdir(self._fileDirPath))
        tags = {name: tag for tag, name in
                self._tagActor.loadTags().get().items()}

        filesTagArray = []
        for fileName in currentFiles:
            if fileName in tags:
                filesTagArray.append({"name": fileName, "tag": tags[fileName]})
            else:
                filesTagArray.append({"name": fileName, "tag": None})

        return filesTagArray

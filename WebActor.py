from subprocess import Popen, PIPE
import logging
import os
import pykka
import re
from bottle import Bottle, template, redirect


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
        total, free = self._getDiskInfo()
        return template('index', items=self._getItems(), totalMem=total,
                        freeMem=free)

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

    def _getDiskInfo(self):
        p = Popen("df -h .", shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        m = re.match("([0-9KMGTP\.]+)[\s]+[0-9KMGTP\.]+[\s]+([0-9KMGTP\.]+)",
                     out.decode('utf-8'))
        total = "N/A"
        free = "N/A"
        if m is not None:
            total = m.group(1)
            free = m.group(2)
        return total, free

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

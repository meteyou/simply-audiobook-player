import pykka
from os.path import join, dirname
from os import listdir
import shutil
from bottle import Bottle, redirect, route, static_file, template, url


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

    def startServer(self):
        self._setup_routes()
        self._app.run(host=self._host, port=self._port)

    def _setup_routes(self):
        @self._app.route('/assets/<filepath:path>', name='assets')
        def assets(filepath):
            return static_file(filepath, root=join(dirname(__file__), 'assets'))

        @self._app.route('/add/<name>', name='add')
        def add(name):
            self._tagActor.addTag(name).get()
            redirect('/')

        @self._app.route('/remove/<tag>', name='remove')
        def remove(tag):
            self._tagActor.removeTag(tag).get()
            redirect('/')

        @self._app.route('/play/<tag>', name='play')
        def play(tag):
            self._tagActor.playByTag(tag)
            return 'Called tagActor with tag: %s\n' % tag

        @self._app.route('/play/<tag>/fromStart', name='play_from_start')
        def play_from_start(tag):
            self._tagActor.playByTag(tag, fromStart=True)
            return 'Called tagActor with tag: %s and fromStart=True\n' % tag

        @self._app.route('/')
        def index():
            total, used, free = shutil.disk_usage(self._fileDirPath)
            return template('index',
                            items=self._getItems(),
                            totalSpace=sizeof_fmt(total),
                            freeSpace=sizeof_fmt(free),
                            url=self._app.get_url,
                            current_page='audiobooks')

    def _getItems(self, **k):
        currentFiles = sorted(listdir(self._fileDirPath))
        tags = {name: tag for tag, name in
                self._tagActor.loadTags().get().items()}

        filesTagArray = []
        for fileName in currentFiles:
            if fileName in tags:
                filesTagArray.append({"name": fileName, "tag": tags[fileName]})
            else:
                filesTagArray.append({"name": fileName, "tag": None})

        return filesTagArray

import json
import logging
import pykka


class TagActor(pykka.ThreadingActor):
    def __init__(self, config, stateActor):
        super(TagActor, self).__init__()

        self.config = config
        self.stateActor = stateActor

        self.tagsFilePath = config.get('TagActor', 'tagsFilePath',
                                       fallback='data/tags.json')

    def playByTag(self, tag, fromStart=False):
        try:
            tags = self.loadTags()
            self.stateActor.playFromLastState(tags[tag], fromStart)
        except KeyError:
            logging.getLogger('sabp').error('No such tag %s' % tag)

    def addTag(self, name):
        tag = self.getTagActor().getTag().get()
        if tag is not None:
            tags = self.loadTags()
            tags[tag] = name
            self.saveTags(tags)

    def removeTag(self, tag):
        tags = self.loadTags()
        del tags[tag]
        self.saveTags(tags)

    def getTagActor(self):
        return pykka.ActorRegistry.get_by_class_name("NfcActor")[0].proxy()

    def loadTags(self):
        try:
            with open(self.tagsFilePath, 'r') as tagsFile:
                return json.load(tagsFile)
        except (IOError, ValueError) as e:
            logging.getLogger('sabp').error('Unable to load tag file %s' %
                                            self.tagsFilePath)
            logging.getLogger('sabp').exception(e)
            return {}

    def saveTags(self, state):
        with open(self.tagsFilePath, 'w') as tagsFile:
            json.dump(state, tagsFile)

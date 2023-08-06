import os

from tw5_server import exceptions, settings


class BaseStorage:
    def __init__(self, name, dir_path=None, wiki_file='tw5.html', **kwargs):
        self.name = name
        self.dir_path = os.path.join(settings.WIKI_DIR, dir_path or name)
        if not os.path.exists(self.dir_path):
            msg = 'dir {} does not exist'.format(self.dir_path)
            raise exceptions.DirNotExist(msg)
        if not os.path.isdir(self.dir_path):
            msg = 'path {} is not a dir'.format(self.dir_path)
            raise exceptions.NotDir(msg)
        self.wiki_file = os.path.join(self.dir_path, wiki_file)

    @classmethod
    def create(cls, name, dir_path=None, wiki_file='tw5.html', **kwargs):
        dir_path = os.path.join(settings.WIKI_DIR, dir_path or name)
        if os.path.exists(dir_path):
            msg = 'dir {} already exists'.format(dir_path)
            raise exceptions.DirAlreadyExist(msg)
        cls._init_storage(dir_path, wiki_file)
        return cls(name, dir_path=dir_path, wiki_file=wiki_file, **kwargs)

    @classmethod
    def _init_storage(cls, dir_path, filename):
        raise NotImplementedError

    def update_wiki(self):
        pass

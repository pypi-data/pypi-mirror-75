import os
import shutil

from git import Repo
from git.util import Actor

from tw5_server import settings
from .base import BaseStorage


class GitStorage(BaseStorage):
    author = Actor('tw5-server', '')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repo = Repo(self.dir_path)

    @classmethod
    def _init_storage(cls, dir_path, filename):
        try:
            repo = Repo.init(dir_path)
            filename = os.path.join(dir_path, filename)
            shutil.copy(settings.EMPTY_TW_FILE, filename)
            repo.index.add(filename)
            repo.index.commit('wiki init', author=cls.author)
        except Exception as err:
            if os.path.exists(dir_path):
                os.removedirs(dir_path)
            raise err

    def update_wiki(self, file_obj):
        with open(self.wiki_file, 'wb') as f:
            shutil.copyfileobj(file_obj, f)
        self.repo.index.add(self.wiki_file)
        self.repo.index.commit('automaticly commit')

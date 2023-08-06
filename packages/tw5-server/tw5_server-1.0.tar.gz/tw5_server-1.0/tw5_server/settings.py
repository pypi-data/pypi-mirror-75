import os

from p_config import Config

if os.environ.get('TW5_SERVER_CONFIG'):
    config = Config(os.environ['TW5_SERVER_CONFIG'])
else:
    config = Config()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

_DEFAULT_TW_FILE = os.path.join(STATIC_DIR, 'empty_tw5.html')
EMPTY_TW_FILE = config.get('SERVER.EMPTY_TW_FILE', _DEFAULT_TW_FILE)

_DEFAULT_WIKI_DIR = os.path.join(os.getcwd(), 'wiki_dir')
WIKI_DIR = os.path.abspath(config.get('SERVER.WIKI_DIR', _DEFAULT_WIKI_DIR))

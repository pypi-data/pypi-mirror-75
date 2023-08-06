from flask import abort, request

from tw5_server.settings import config
"""
1. use basic auth to protect wiki
2. tiddly-wiki will save username
3. tiddly-wiki save will use password filled in form rather than basic auth
"""


class Auth:
    def __init__(self, app):
        self._wiki_credential_mapping = {
            item['name']: {
                'view_key': item['view_key'],
                'write_key': item['write_key']
            }
            for item in config['WIKI']
        }
        self.app = app

        @app.before_request
        def common_auth_required():
            if not self.check_view_permission():
                abort(401)

    def _check_wiki_key(self, wiki_name=None, key=None, key_type=None):
        authorization = request.authorization or {}
        if wiki_name is None:
            wiki_name = authorization.get('username')
        if key is None:
            key = authorization.get('password')
        credential = self._wiki_credential_mapping.get(wiki_name, {})
        return credential.get(key_type) == key

    def check_view_permission(self, wiki_name=None, key=None):
        return self._check_wiki_key(wiki_name, key, 'view_key') or \
            self.check_write_permission(wiki_name, key)

    def check_write_permission(self, wiki_name=None, key=None):
        return self._check_wiki_key(wiki_name, key, 'write_key')

import sys

import click
from flask import (Flask, abort, make_response, render_template, request,
                   send_file)

from tw5_server import exceptions
from tw5_server.storage.git import GitStorage
from .auth import Auth

app = Flask(__name__)
auth = Auth(app)


@app.cli.command("create-wiki")
@click.argument("name")
def create_wiki(name):
    storage = GitStorage.create(name)
    sys.stdout.write('wiki "{}" is created. dir is {}'.format(
        name, storage.dir_path))


@app.errorhandler(401)
def not_authroized(error):
    response = make_response(render_template('401.html'), 401)
    response.headers['WWW-Authenticate'] = 'Basic realm=""'
    return response


@app.errorhandler(403)
def permission_denied(error):
    return make_response(render_template('403.html'), 403)


@app.errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html'), 404)


@app.route('/<string:wiki_name>')
def index(wiki_name):
    if not auth.check_view_permission(wiki_name):
        abort(401)
    try:
        storage = GitStorage(wiki_name)
        return send_file(storage.wiki_file)
    except exceptions.DirNotExist:
        abort(404)


@app.route('/<string:wiki_name>/store', methods=['POST'])
def update_wiki(wiki_name):
    # check auth
    params = request.form.get('UploadPlugin', '').split(';')
    params = (param for param in params if '=' in param)
    param_dict = dict(param.split('=', 1) for param in params)
    password = param_dict.get('password')
    if not auth.check_write_permission(wiki_name, password):
        abort(401)
    # check file
    file_obj = request.files.get('userfile')
    if not file_obj or file_obj.mimetype != 'text/html':
        abort(400)
    # update wiki
    try:
        storage = GitStorage(wiki_name)
    except exceptions.DirNotExist:
        abort(404)
    storage.update_wiki(file_obj.stream)
    return '0 - '

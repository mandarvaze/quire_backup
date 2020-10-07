import logging
import os
import sys
import requests
from flask import request, Flask, jsonify
from loguru import logger
from quire import get_tokens, get_project_list, get_project_json

app = Flask(__name__)
CSRF_TOKEN = os.environ.get("CSRF_TOKEN", None)
CLIENT_ID = os.environ.get("CLIENT_ID", None)
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
QUIRE_TOKEN_URL = 'https://quire.io/oauth/token'

AUTH_TOKEN = None
REFRESH_TOKEN = None


@app.route('/quire_callback', methods=['GET', 'POST'])
def quire_oauth2_callback():
    global AUTH_TOKEN, REFRESH_TOKEN
    # prevent Cross-Site Request Forgery (CSRF) attacks.
    if CSRF_TOKEN and request.args['state'] != CSRF_TOKEN:
        return {'error': 'Invalid state'}
    if 'error' in request.args:
        return {'error': 'User rejected auth request'}
    if "code" in request.args:
        AUTH_TOKEN, REFRESH_TOKEN = get_tokens(
            CLIENT_ID, CLIENT_SECRET, request.args['code'], QUIRE_TOKEN_URL)
        logger.debug(f"Auth Token: {AUTH_TOKEN}")
        return 'Success. You can close this browser now.'


@app.route('/quire_projects', methods=['GET'])
def quire_projects():
    if not REFRESH_TOKEN:
        return {"message": "Tokens not initialized."}, 403

    if AUTH_TOKEN:
        proj_list = get_project_list(AUTH_TOKEN)

        if 'error' in proj_list:
            return proj_list, 400
        return jsonify(proj_list)

    return 'success'


@app.route('/quire_backup/<projectname>', methods=['GET'])
def quire_backup(projectname: str):
    if not REFRESH_TOKEN:
        return {"message": "Tokens not initialized."}, 403

    if AUTH_TOKEN:
        proj_json = get_project_json(projectname, AUTH_TOKEN)
        return jsonify(proj_json)

    return 'error', 400


if __name__ == '__main__':
    required_env_vars = [CLIENT_ID, CLIENT_SECRET]
    run = True

    for env_var in required_env_vars:
        if env_var is None:
            print(f'Please set environment variable: {env_var}')
            if run:
                run = False
    if run:
        logger.configure(
            handlers=[
                {"sink": sys.stdout, "level": logging.DEBUG},
                # "format": format_record},
                {
                    "sink": "./quire_backup.log",
                    "rotation": "daily",
                    "level": logging.DEBUG,
                    #  "format": format_record,
                },
            ]
        )
        app.run(host='localhost', port=3000)

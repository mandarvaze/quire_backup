
"""
All the quire.io related functions are here
"""
import requests
from loguru import logger

QUIRE_BASE_URL = 'https://quire.io/api'
PROJ_LIST_URL = '/project/list'


class QuireProject():

    def __init__(self, prj_id: str, auth_token: str):
        self.data = {}
        self.prj_id = prj_id
        self.auth_token = auth_token
        self.auth_header = {'Authorization': f'Bearer {auth_token}'}
        self.data['otype'] = 'Project'
        self.data['id'] = self.prj_id

    def _get_members(self):
        pass

    def _get_basic_info(self):
        url = f'{QUIRE_BASE_URL}/project/id/{self.prj_id}'

        logger.debug(f'Trying to get {url}')
        resp = requests.get(url, headers=self.auth_header)
        if resp.status_code == 200:
            self.data.update(resp.json())
        else:
            logger.debug(
                f"Unable to get project info for {self.prj_id} : {resp.text}")

    def _get_users(self):
        pass

    def _get_tasks(self):
        pass

    def _get_partners(self):
        pass

    def _get_boards(self):
        pass

    def get_backup_json(self):
        self._get_basic_info()
        self._get_members()
        self._get_users()
        self._get_tasks()
        self._get_partners()
        self._get_boards()

        return self.data


def get_tokens(
        client_id: str,
        client_secret: str,
        code: str,
        quire_token_url: str):
    """
    Get Access and Refresh Tokens from quire.io
    """

    access_token = None
    refresh_token = None

    auth_token_json = {
        'grant_type': "authorization_code",
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret
    }
    resp = requests.post(quire_token_url, data=auth_token_json, headers={
                         "Content-Type": "application/x-www-form-urlencoded"})
    if resp.status_code == 200:
        access_token = resp.json()['access_token']
        refresh_token = resp.json()['refresh_token']
    else:
        logger.error(f"Unable to get access token: {resp.text}")

    return access_token, refresh_token


def get_project_list(auth_token: str):
    headers = {'Authorization': f'Bearer {auth_token}'}
    resp = requests.get(f'{QUIRE_BASE_URL}{PROJ_LIST_URL}', headers=headers)
    if resp.status_code != 200:
        return {'error': resp.text}

    return resp.json()


def get_project_json(prj_id: str, auth_token: str):
    """
    In order for the JSON to be compatible with restore/Import functionality :
    - members
    - tasks
    - boards
    - users
    - tags
    - partners
    """
    proj = QuireProject(prj_id, auth_token)
    return proj.get_backup_json()

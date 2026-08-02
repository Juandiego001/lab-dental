from flask_babel import gettext
from werkzeug.exceptions import HTTPException
import requests


def get_aligner(serial_number: str):
    '''Get aligner by serial number'''

    response = requests.get(
        f'https://vehicle365.org/read/aligner/v1/?serialNumber={serial_number}&username=andresleon')
    if response.status_code == 404:
        raise HTTPException(gettext('alignerNotFound'))
    return response.json()


def get_last_version():
    '''Get last version'''

    response = requests.get(
        'https://vehicle365.org/read/latest_software_version/v1')
    response.raise_for_status()
    return response.json()


def send_stage_command(serial_number: str):
    '''Send stage command'''

    last_version_dict = get_last_version()
    response = requests.post(
        'https://vehicle365.org/create/immediate_stage_of_software_update/v1',
        json={
            "serialNumber": serial_number,
            "version": {
                "semantic": last_version_dict['semantic']
            },
            "path": last_version_dict['path']

        }
    )
    response.raise_for_status()


def send_unstage_command(serial_number: str):
    '''Send unstage command'''

    response = requests.post(
        'https://vehicle365.org/delete/immediate_unstage_of_software_update/v1',
        json={
            "serialNumber": serial_number
        }
    )
    response.raise_for_status()


def send_cloud_command(serial_number: str):
    '''Send cloud command'''

    response = requests.post(
        'https://vehicle365.org/cmd/aligner_check_now/v1',
        json={
            "serialNumber": serial_number
        }
    )
    response.raise_for_status()

import logging
import os

import requests
from dotenv import load_dotenv
from marshmallow import ValidationError

from .exceptions import *
from .schemas import check_verification_input_schema, create_verification_input_schema, \
    check_verification_output_schema, create_verification_output_schema
from .utils import encode

logging.basicConfig(
    filename='debug.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

load_dotenv()


class Verify:
    def __init__(self, env: str, app_key: str, app_secret: str):
        self.env = env
        self.app_key = app_key
        self.app_secret = app_secret
        self.url = self.get_root_url()

    def create_verification(self, channel: str, template_name: str, to: str,
                            subject_params: dict = None, body_params: dict = None):
        variables = locals()
        variables.pop('self', None)
        try:
            data = create_verification_input_schema.load(variables)
        except ValidationError as e:
            invalid_parameters['invalid_params'] = e.messages
            return invalid_parameters
        token = encode(self.app_key, self.app_secret)
        headers = {'Authorization': token}
        response = requests.post(url=self.url + '/verifications', data=data, headers=headers)
        if response.status_code // 100 == 2:
            return create_verification_output_schema.dump(response.json())
        return response.json()

    def check_verification(self, channel: str, to: str, code: str):
        variables = locals()
        variables.pop('self', None)
        try:
            data = check_verification_input_schema.load(variables)
        except ValidationError as e:
            invalid_parameters['invalid_params'] = e.messages
            return invalid_parameters
        token = encode(self.app_key, self.app_secret)
        headers = {'Authorization': token}
        response = requests.post(url=self.url + '/verifications-check', data=data, headers=headers)
        if response.status_code // 200 == 2:
            return check_verification_output_schema.dump(response.json())
        return response.json()

    def get_root_url(self):
        url = os.getenv(f'{self.env.upper()}_URL')
        if not url:
            logging.error(f'No environment named {self.env}')
            exit(1)
        return url

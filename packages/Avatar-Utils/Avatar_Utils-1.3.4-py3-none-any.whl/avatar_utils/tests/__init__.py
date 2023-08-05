import copy
import logging
from unittest import TestCase

import flask
import requests

from avatar_utils.tests.Env import DevEnv

logger = logging.getLogger(__name__)


class AbstractApp:
    client = None
    headers = {'Content-type': 'application/json'}

    def post(self, url, data=dict()) -> flask.Response:
        return self.client.post(url, json=data, headers=self.headers)

    def get(self, url, data=dict()) -> flask.Response:
        return self.client.get(url, json=data, headers=self.headers)

    def register(self, username, email, password, confirm) -> flask.Response:
        return self.post('/register', data=dict(username=username, email=email, password=password, confirm=confirm))

    def login(self, username, password) -> flask.Response:
        return self.post('/login', data=dict(username=username, password=password))

    def logout(self) -> flask.Response:
        return self.post('/logout')

    def delete(self, user_id, password):
        return self.post('/user/delete', data=dict(user_id=user_id, password=password))

    def rprint(self, response):
        if not isinstance(response, flask.Response):
            logger.warning(f'rprint prints only flask.Response class data')
            return

        json = response.json
        if json:
            logger.debug(json)
        else:
            logger.debug(response.data.decode())


class RemoteApp(AbstractApp):
    client = requests

    # default env, specified once per whole test class
    default_env = DevEnv()

    # current env, could be changed in every test fuction
    current_env = copy.deepcopy(default_env)

    @property
    def base_url(self):
        return self.current_env.base_url

    def post(self, url, data=dict()) -> flask.Response:
        res = super().post(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    def get(self, url, data=dict()) -> flask.Response:
        res = super().get(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    # TODO transfer headers
    @staticmethod
    def convert_to_flask_response(response) -> flask.Response:
        res = flask.Response(
            response=response.text,
            status=response.status_code,
            mimetype=response.headers['content-type']
        )

        return res


class UnitTest(TestCase, AbstractApp):
    app = None
    db = None

    def setUp(self):
        TestCase.setUp(self)
        try:
            print('SQLALCHEMY_DATABASE_URI: %s' % self.app.config['SQLALCHEMY_DATABASE_URI'])
        except KeyError:
            pass

        self.assertFalse(self.app is None)
        self.assertFalse(self.client is None)
        self.assertTrue(self.app.config['TESTING'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
        super().setUp()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
        TestCase.tearDown(self)


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db

    app.logger.handlers.clear()
    logging.basicConfig(level=app.config['LOGGING_LEVEL'],
                        format='%(asctime)s %(levelname)s %(message)s')


class IntegrationTest(TestCase, RemoteApp):

    def setUp(self):
        super().setUp()

        # reset current env
        self.current_env = copy.deepcopy(RemoteApp.default_env)

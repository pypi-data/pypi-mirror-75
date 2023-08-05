from unittest import TestCase
from flask import Flask
from flask_auth_service_mongo import config
from ...models import User
from ...utils import Payload, password_hash, password_match,\
    token_decode, token_generate


class TestPayload(TestCase):
    def test_new_full(self):
        params = ('error', 'user_id')
        payload = Payload(*params)
        self.assertEqual(params[0], payload.error)
        self.assertEqual(params[1], payload.user_id)

    def test_new_nullable(self):
        payload = Payload()
        self.assertIsNone(payload.error)
        self.assertIsNone(payload.user_id)


class TestPassword(TestCase):
    """Pruebas del generador del hash y el match para la contraseña"""

    def test_hash_and_match(self):
        param = 'password'
        hashpw = password_hash(param)

        self.assertIsInstance(hashpw, str)
        self.assertNotEqual(hashpw, param)

        matchpw = password_match(param, hashpw)

        self.assertIsInstance(matchpw, bool)
        self.assertTrue(matchpw)

        matchpw = password_match('param', hashpw)

        self.assertIsInstance(matchpw, bool)
        self.assertFalse(matchpw)


class TestToken(TestCase):
    """Pruebas para el generador y el decode del token"""

    def test_generate_and_decode(self):
        # Crea el contexto del app flask
        app = Flask(__name__)
        config.SECRET_KEY = 'not-secret'

        with app.app_context():
            user = User(id='id')

            # generar token
            token = token_generate(user)
            self.assertIsInstance(token, str)

            # Decode Ok token
            payload = token_decode(token)
            self.assertIsInstance(payload, Payload)
            self.assertIsNone(payload.error)
            self.assertEqual(payload.user_id, 'id')

            # Decode expired token
            token = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMjE'
                     '5NzYsImlhdCI6MTU3NjAxODM3Niwic3ViIjoiNWRmMDIxYmU1Y2I0Y2Z'
                     'hZDgyMzM5MTg4Iiwicm9sIjoiYWRtaW4ifQ.PYY_7TRhSyd0_H_tXGBt'
                     'WCSm2K_pPuNjyOk4NERgNrk')
            payload = token_decode(token)
            self.assertIsInstance(payload, Payload)
            self.assertEqual(payload.error, 'signature_expired')
            self.assertIsNone(payload.user_id)

            # Decode expired token
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMjE'
            payload = token_decode(token)
            self.assertIsInstance(payload, Payload)
            self.assertEqual(payload.error, 'invalid_token')
            self.assertIsNone(payload.user_id)

import datetime
import unittest

from hash_chain.app.extensions import db
from hash_chain.app.modules.users.models import User
from hash_chain.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_access_token()
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_access_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_access_token(auth_token.decode("utf-8")).value.get('public_id') == user.public_id)


if __name__ == '__main__':
    unittest.main()

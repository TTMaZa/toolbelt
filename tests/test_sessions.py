# -*- coding: utf-8 -*-
import unittest
import pytest

from requests_toolbelt.sessions import BasedSession
from . import get_betamax


class TestBasedSession(unittest.TestCase):
    def test_with_base(self):
        session = BasedSession('https://httpbin.org/')
        recorder = get_betamax(session)
        with recorder.use_cassette('simple_get_request'):
            response = session.get('/get')
        response.raise_for_status()

    def test_without_base(self):
        session = BasedSession()
        with pytest.raises(ValueError):
            session.get('/')

    def test_override_base(self):
        session = BasedSession('https://www.google.com')
        recorder = get_betamax(session)
        with recorder.use_cassette('simple_get_request'):
            response = session.get('https://httpbin.org/get')
        response.raise_for_status()
        assert response.json()['headers']['Host'] == 'httpbin.org'

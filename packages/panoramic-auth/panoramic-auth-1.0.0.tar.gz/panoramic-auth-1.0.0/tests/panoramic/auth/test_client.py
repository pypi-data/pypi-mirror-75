import datetime

import freezegun
import pytest
import responses

from panoramic.auth.client import (
    _DEFAULT_SCOPE,
    _DEFAULT_TOKEN_URL,
    _SCOPE_ENV_NAME,
    _TOKEN_URL_ENV_NAME,
    OAuth2Error,
    OAuth2Session,
)


@pytest.mark.parametrize(
    ['client_id', 'client_secret'],
    [('', 'client-secret'), (None, 'client-secret'), ('client-id', ''), ('client-id', None),],
)
def test_session_throws_when_no_client_id(client_id, client_secret):
    with pytest.raises(OAuth2Error):
        OAuth2Session(client_id, client_secret)


@responses.activate
@freezegun.freeze_time('2020-01-01')
def test_session_no_kwargs_no_env_uses_defaults():
    responses.add(
        responses.POST,
        _DEFAULT_TOKEN_URL,
        json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': _DEFAULT_SCOPE},
    )

    token = OAuth2Session('client-id', 'client-secret').fetch_token()

    assert token == {
        'token_type': 'Bearer',
        'expires_at': 1577840400,
        'expires_in': 3600,
        'access_token': 'TOKEN',
        'scope': [_DEFAULT_SCOPE],
    }


@responses.activate
@freezegun.freeze_time('2020-01-01')
def test_session_no_kwargs_uses_env(monkeypatch):
    monkeypatch.setenv(_TOKEN_URL_ENV_NAME, 'https://test-url/token')
    monkeypatch.setenv(_SCOPE_ENV_NAME, 'test-scope')

    responses.add(
        responses.POST,
        'https://test-url/token',
        json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': 'test-scope'},
    )

    token = OAuth2Session('client-id', 'client-secret').fetch_token()

    assert token == {
        'token_type': 'Bearer',
        'expires_at': 1577840400,
        'expires_in': 3600,
        'access_token': 'TOKEN',
        'scope': ['test-scope'],
    }


@responses.activate
@freezegun.freeze_time('2020-01-01')
def test_session_uses_kwargs(monkeypatch):
    responses.add(
        responses.POST,
        'https://test-url/token',
        json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': 'test-scope'},
    )

    token = OAuth2Session(
        'client-id', 'client-secret', token_url='https://test-url/token', scope='test-scope'
    ).fetch_token()

    assert token == {
        'token_type': 'Bearer',
        'expires_at': 1577840400,
        'expires_in': 3600,
        'access_token': 'TOKEN',
        'scope': ['test-scope'],
    }


@responses.activate
def test_session_request_fetches_token():
    responses.add(
        responses.POST,
        _DEFAULT_TOKEN_URL,
        json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': _DEFAULT_SCOPE},
    )

    responses.add(
        responses.GET,
        'https://husky-secure/data',
        json={'result': 'data'},
        adding_headers={'Authorization': 'Bearer TOKEN'},
    )

    resp = OAuth2Session('client-id', 'client-secret').get('https://husky-secure/data')

    assert resp.json() == {'result': 'data'}


@responses.activate
def test_session_request_fetches_token_only_once():
    responses.add(
        responses.POST,
        _DEFAULT_TOKEN_URL,
        json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': _DEFAULT_SCOPE},
    )

    responses.add(
        responses.GET,
        'https://husky-secure/data',
        json={'result': 'data'},
        adding_headers={'Authorization': 'Bearer TOKEN'},
    )

    responses.add(
        responses.GET,
        'https://husky-secure/status',
        json={'status': 'RUNNING'},
        adding_headers={'Authorization': 'Bearer TOKEN'},
    )

    session = OAuth2Session('client-id', 'client-secret')
    resp1 = session.get('https://husky-secure/data')
    resp2 = session.get('https://husky-secure/status')

    assert resp1.json() == {'result': 'data'}
    assert resp2.json() == {'status': 'RUNNING'}
    assert len(responses.calls) == 3


@responses.activate
def test_session_request_refetches_token_when_expired():
    """Use token successfully, let it expire, refetch token and use new token."""
    with freezegun.freeze_time('2020-01-01') as frozen_time:

        def _advance_time(*args):
            frozen_time.tick(delta=datetime.timedelta(hours=2))
            return (200, {}, '{"result": "data"}')

        responses.add(
            responses.POST,
            _DEFAULT_TOKEN_URL,
            json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': _DEFAULT_SCOPE},
        )

        responses.add_callback(
            responses.GET, 'https://husky-secure/data', callback=_advance_time,
        )

        responses.add(
            responses.POST,
            _DEFAULT_TOKEN_URL,
            json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'NEW-TOKEN', 'scope': _DEFAULT_SCOPE},
        )

        responses.add(
            responses.GET,
            'https://husky-secure/status',
            json={'status': 'RUNNING'},
            adding_headers={'Authorization': 'Bearer NEW-TOKEN'},
        )

        session = OAuth2Session('client-id', 'client-secret')
        resp1 = session.get('https://husky-secure/data')
        resp2 = session.get('https://husky-secure/status')

        assert resp1.json() == {'result': 'data'}
        assert resp2.json() == {'status': 'RUNNING'}


@freezegun.freeze_time('2020-01-01')
def test_session_wraps_fetch_token_error():
    session = OAuth2Session('client-id', 'client-secret')

    def mock_fetch_token(*_, **__):
        raise Exception('test')

    session.fetch_token = mock_fetch_token

    with pytest.raises(OAuth2Error):
        session.get('https://husky-secure/data')


@responses.activate
def test_session_wraps_refetch_token_error():
    """Use token successfully, let it expire, refetch token and use new token."""
    with freezegun.freeze_time('2020-01-01') as frozen_time:

        session = OAuth2Session('client-id', 'client-secret')

        def mock_fetch_token(*_, **__):
            raise Exception('test')

        def _advance_time_break_fetch_token(*args):
            frozen_time.tick(delta=datetime.timedelta(hours=2))
            session.fetch_token = mock_fetch_token
            return (200, {}, '{"result": "data"}')

        responses.add(
            responses.POST,
            _DEFAULT_TOKEN_URL,
            json={'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'TOKEN', 'scope': _DEFAULT_SCOPE},
        )

        responses.add_callback(
            responses.GET, 'https://husky-secure/data', callback=_advance_time_break_fetch_token,
        )

        session.get('https://husky-secure/data')

        with pytest.raises(OAuth2Error):
            resp2 = session.get('https://husky-secure/status')

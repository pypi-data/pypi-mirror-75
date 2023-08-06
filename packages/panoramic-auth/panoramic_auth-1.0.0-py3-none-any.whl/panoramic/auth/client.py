import logging
import os

from typing import Any, Dict, Optional
from urllib.parse import urljoin

from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import OAuth2Error as OauthlibError
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests import Session
from requests_oauthlib import OAuth2Session as OauthlibSession


_TOKEN_URL_ENV_NAME = 'PANORAMIC_AUTH_TOKEN_URL'
_SCOPE_ENV_NAME = 'PANORAMIC_AUTH_SCOPE'
_DEFAULT_TOKEN_URL = 'https://id.panoramichq.com/oauth2/auscsj124wDoFObOJ4x6/v1/token'
_DEFAULT_SCOPE = 'platform'


logger = logging.getLogger(__name__)


class OAuth2Error(Exception):

    """Wrapper error class so we don't leak implementation details."""


class OAuth2Session(OauthlibSession):

    _client_secret: str
    _token_url: str

    def __init__(
        self, client_id: str, client_secret: str, *, scope: Optional[str] = None, token_url: Optional[str] = None
    ):
        if not client_id:
            raise OAuth2Error(f'Missing client_id value')

        if not client_secret:
            raise OAuth2Error(f'Missing client_secret value')

        if scope is None:
            scope = os.environ.get(_SCOPE_ENV_NAME, _DEFAULT_SCOPE)

        if token_url is None:
            token_url = os.environ.get(_TOKEN_URL_ENV_NAME, _DEFAULT_TOKEN_URL)

        assert token_url is not None

        self._client_secret = client_secret
        self._token_url = token_url

        super().__init__(client=BackendApplicationClient(client_id=client_id, scope=_DEFAULT_SCOPE))

    def _request(self, *args, **kwargs):
        return super().request(*args, **kwargs)

    def fetch_token(self):
        """Fetch token and store it on session"""
        return super().fetch_token(self._token_url, client_secret=self._client_secret)

    def request(self, *args, auth: Any = None, **kwargs):
        """Wrap request method from oauthlib/requests."""

        # Auth already worked out (e.g. fetch_token call)
        if auth is not None:
            return self._request(*args, auth=auth, **kwargs)

        # Request missing access token, need to fetch it
        if not self.token:
            logger.debug('Fetching access token before first request.')
            try:
                self.fetch_token()
            except Exception:
                error_msg = 'Failed fetching access token before first request.'
                logger.exception(error_msg)
                raise OAuth2Error(error_msg)

        try:
            # Perform original request
            logger.debug('Sending request with OAuth2 access token.')
            return self._request(*args, **kwargs)
        except TokenExpiredError as e:
            logger.debug('Access token expired, getting new one.')

            try:
                # Access token expired, fetch it again
                self.fetch_token()
            except Exception:
                error_msg = 'Failed refetching access token after expiry.'
                logger.exception(error_msg)
                raise OAuth2Error(error_msg)

            # Perform ooriginal request with refetched token
            logger.debug('Refetched access token, retrying request.')
            return self._request(*args, **kwargs)


class OAuth2Client:
    def __init__(
        self, client_id: str, client_secret: str, *, scope: Optional[str] = None, token_url: Optional[str] = None
    ):
        self.session = OAuth2Session(client_id, client_secret, scope=scope, token_url=token_url)
        super().__init__()

    def fetch_token(self):
        """Fetch token and store it on session"""
        return self.session.fetch_token()

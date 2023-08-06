"""Tests for certbot_dns_aliyun.dns_aliyun."""

import unittest

try:
    import mock
except ImportError: # pragma: no cover
    from unittest import mock # type: ignore
from requests.exceptions import HTTPError
from requests.exceptions import RequestException

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.tests import util as test_util

DOMAIN_NOT_FOUND = Exception('No domain found')
GENERIC_ERROR = RequestException
LOGIN_ERROR = HTTPError('400 Client Error: ...')

API_KEY = 'foo'
SECRET = 'bar'


class AuthenticatorTest(test_util.TempDirTestCase,
                        dns_test_common_lexicon.BaseLexiconAuthenticatorTest):

    def setUp(self):
        super(AuthenticatorTest, self).setUp()

        from certbot_dns_aliyun.dns_aliyun import Authenticator

        path = os.path.join(self.tempdir, 'file.ini')
        dns_test_common.write({"aliyun_api_key": API_KEY, "aliyun_secret_key": SECRET}, path)

        self.config = mock.MagicMock(aliyun_credentials=path,
                                     aliyun_propagation_seconds=0)  # don't wait during tests

        self.auth = Authenticator(self.config, "aliyun")

        self.mock_client = mock.MagicMock()
        # _get_aliyun_client | pylint: disable=protected-access
        self.auth._get_aliyun_client = mock.MagicMock(return_value=self.mock_client)


class AliyunLexiconClientTest(unittest.TestCase, dns_test_common_lexicon.BaseLexiconClientTest):

    def setUp(self):
        from certbot_dns_aliyun.dns_aliyun import _AliyunLexiconClient

        self.client = _AliyunLexiconClient(API_KEY, SECRET, 0)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    unittest.main()  # pragma: no cover

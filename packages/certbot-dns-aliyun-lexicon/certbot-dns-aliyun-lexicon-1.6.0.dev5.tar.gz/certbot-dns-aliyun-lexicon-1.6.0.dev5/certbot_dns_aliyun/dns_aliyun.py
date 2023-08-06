"""DNS Authenticator for Aliyun DNS."""
import logging

from lexicon.providers import aliyun
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

import tldextract

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://help.aliyun.com/knowledge_detail/38738.html'


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Aliyun DNS

    This Authenticator uses the Aliyun DNS API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using Aliyun for DNS).'
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=20)
        add('credentials', help='Aliyun credentials INI file.')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Aliyun API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Aliyun credentials INI file',
            {
                'api-key': 'API key for Aliyun account, obtained from {0}'.format(ACCOUNT_URL),
                'secret-key': 'Secret key for Aliyun account, obtained from {0}'
                              .format(ACCOUNT_URL)
            }
        )

    def _perform(self, domain, validation_name, validation):
        registered_domain = tldextract.extract(domain).registered_domain
        self._get_aliyun_client().add_txt_record(registered_domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        registered_domain = tldextract.extract(domain).registered_domain
        self._get_aliyun_client().del_txt_record(registered_domain, validation_name, validation)

    def _get_aliyun_client(self):
        return _AliyunLexiconClient(self.credentials.conf('api-key'),
                                    self.credentials.conf('secret-key'),
                                    self.ttl)


class _AliyunLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Aliyun via Lexicon.
    """

    def __init__(self, api_key, secret_key, ttl):
        super(_AliyunLexiconClient, self).__init__()

        config = dns_common_lexicon.build_lexicon_config('aliyun', {
            'ttl': ttl,
        }, {
            'auth_key_id': api_key,
            'auth_secret': secret_key,
        })

        self.provider = aliyun.Provider(config)

    def _handle_http_error(self, e, domain_name):
        hint = None
        if str(e).startswith('400 Client Error:'):
            hint = 'Are your API key and Secret key values correct?'

        return errors.PluginError('Error determining zone identifier for {0}: {1}.{2}'
                                  .format(domain_name, e, ' ({0})'.format(hint) if hint else ''))

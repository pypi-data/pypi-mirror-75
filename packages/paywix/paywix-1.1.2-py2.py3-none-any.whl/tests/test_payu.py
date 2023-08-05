import unittest
from unittest.mock import MagicMock
from paywix.payu import Payu


class TestPayu(unittest.TestCase):

    def test_payu_transaction(self):
        payu_config = MagicMock()
        merchant_key = payu_config.get('merchant_key')
        merchant_salt = payu_config.get('merchant_salt')
        surl = payu_config.get('success_url')
        furl = payu_config.get('failure_url')
        mode = "test"
        payu = Payu(merchant_key, merchant_salt, surl, furl, mode)



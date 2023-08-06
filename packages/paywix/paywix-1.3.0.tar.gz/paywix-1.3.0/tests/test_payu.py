import unittest
from unittest.mock import MagicMock
from paywix.payu import Payu


class TestPayu(unittest.TestCase):

    def test_payu_transaction(self):
        PAYU_CONFIG = {
            "merchant_key": "3o6jgxhp",
            "merchant_salt": "67bAgZX1B3",
            "mode": "test",
            "success_url": "http://127.0.0.1:8000/payu/success",
            "failure_url": "http://127.0.0.1:8000/payu/failure"
        }
        merchant_key = PAYU_CONFIG.get('merchant_key')
        merchant_salt = PAYU_CONFIG.get('merchant_salt')
        success_url = PAYU_CONFIG.get('success_url')
        failure_url = PAYU_CONFIG.get('failure_url')
        auth_header = "m9iqezZAFsJ+VE8n/mkLoq86bfV1m9KbxS+IwsHEHic="
        payu = Payu(merchant_key, merchant_salt, success_url,
                    failure_url, mode="live", auth_header=auth_header)
        # payment_Resp = payu.getPaymentResponse({"ids": ['172b0970-d073-11ea-8a7c-f0189853078a']})
        # payment_Resp1 = payu.chkMerchantTxnStatus(
        #     {"ids": ['172b0970-d073-11ea-8a7c-f0189853078a', '172b0970-d073-11ea-8a7c-f0189853078a']})

        # refund_amount = payu.refundPayment({'payu_id': 58872009, 'amount': 5})

        # refund_details_1 = payu.getRefundDetails({'refund_id': 190783})
        refund_details_2 = payu.getRefundDetailsByPayment({'payu_id': 190783})

        print(refund_details_2)

        


        # data1 = payu.get_merchant_transaction_status(['172b0970-d073-11ea-8a7c-f0189853078a',
        #                                             '172b0970-d073-11ea-8a7c-f0189853078a'])
        # data2 = payu.get_paymentresponse(['172b0970-d073-11ea-8a7c-f0189853078a',
        #                                 '172b0970-d073-11ea-8a7c-f0189853078a'])

        # data3 = payu.refund_amount(58872009, 130)
        # data4 = payu.refund_details(58872009)
        # print(data4)



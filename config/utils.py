import requests
from django.conf import settings
import logging
import random

logger = logging.getLogger(__name__)

class PayStack(object):
    headers = headers = {'Authorization': 'Bearer %s' % settings.PAYSTACK_SECRET_KEY,
                         'Content-Type': 'application/json'}

    def create_customer(self, data):
        r = requests.post(settings.PAYSTACK_BASE_URL +
                          '/customer', json=data, headers=self.headers)
        if r.status_code >= 400:
            raise (requests.HTTPError)
        return r.json()['data']['customer_code']

    def validate_transaction(self, ref):
        r = requests.get(settings.PAYSTACK_BASE_URL +
                         '/transaction/verify/' + ref, headers=self.headers)
        logger.info(r.status_code)
        if r.status_code >= 400:
            logger.info(r.text)
            print(r.text)
            r.raise_for_status()
        print(r.json())
        data = r.json()['data']
        if r.json()['status']:
            return dict(authorization_code=data['authorization']['authorization_code'],
                        amount_paid=data['amount'] / 100)
        return None

    def initialize_transaction(self, data):
        """
        Initializing transaction from server us
        :data : {
            'reference','email','amount in kobo',
            'callback_url'
        }
        """
        r = requests.post(settings.PAYSTACK_BASE_URL +
                          '/transaction/initialize', json=data, headers=self.headers)
        if r.status_code >= 400:
            logger.info(r.text)
            print(r.text)
            r.raise_for_status()
        print(r.json())
        if r.json()['status']:
            return r.json()['data']
        return {}

    def recurrent_charge(self, data):
        """
        When attempting to bill an existing customers that has already paid through us
        :data : {
            'authorization_code','email','amount'
        }
        """
        r = requests.post(settings.PAYSTACK_BASE_URL +
                          '/transaction/charge_authorization', json=data, headers=self.headers)
        if r.status_code >= 400:
            r.raise_for_status()
        print(r.json())
        logger.info(r.json())
        if r.json()['status']:
            return True
        return False

    def create_recipient(self, payout_details):
        """bank, account_id,account_name"""
        req = requests.post(
            settings.PAYSTACK_BASE_URL +
            '/transferrecipient',
            json={
                "type": "nuban",
                "name": payout_details.account_name,
                "description": payout_details.account_name,
                "account_number": payout_details.account_id,
                "bank_code": self.get_bank_code(payout_details.bank),
                "currency": "NGN",
            },
            headers=self.headers)
        if req.status_code >= 400:
            req.raise_for_status()
        return req.json()['data']

    def initialize_transfer(self, amount, recipient, reason):
        new_amount = amount * 100
        req = requests.post(
            settings.PAYSTACK_BASE_URL +
            '/transfer',
            json={"source": "balance", "reason": reason,
                  "amount": amount, "recipient": recipient},
            headers=self.headers)
        if req.status_code >= 400:
            req.raise_for_status()
        return req.json()

    def verify_transfer(self, transfer_recipient, code):
        """verify transaction"""
        req = requests.post(
            settings.PAYSTACK_BASE_URL +
            '/transfer/finalize_transfer',
            json={"transfer_code": transfer_recipient, "otp": code},
            headers=self.headers)
        if req.status_code >= 400:
            req.raise_for_status()
        return req.json()['data']

    def enable_otp(self, status=True, code=None):
        url = '/transfer/enable_otp'
        if not status:
            url = '/transfer/disable_otp'
        if code:
            url = '/transfer/disable_otp_finalize'
        json = {}
        if code:
            json = {"otp": code}
        req = requests.post(
            settings.PAYSTACK_BASE_URL +
            url, json=json, headers=self.headers)
        if req.status_code >= 400:
            req.raise_for_status()
        return req.json()['data']

    def resend_otp(self, transfer_recipient):
        req = requests.post(settings.PAYSTACK_BASE_URL +
                            '/transfer/resend_otp',
                            json={'transfer_code': transfer_recipient},
                            headers=self.headers)
        if req.status_code >= 400:
            req.raise_for_status()
        return req.json()['data']

    def get_transfer(self, transfer_recipient):
        """Fetch the transfer for a given recipient"""
        req = requests.get(settings.PAYSTACK_BASE_URL +
                           '/transfer/' + transfer_recipient, headers=self.headers)
        if req.status_code >= 400:
            raise (requests.HTTPError)
        data = req.json()
        return data['data']

    def get_bank_code(self, bank_name):
        options = {
            'Citibank': '023',
            'Access Bank': '044',
            'Diamond Bank': '063',
            'Ecobank Nigeria': '050',
            'Enterprise Bank': '084',
            'Fidelity Bank Nigeria': '070',
            'First Bank of Nigeria': '011',
            'First City Monument Bank': '214',
            'Guaranty Trust Bank': '058',
            'Heritage Bank': '030',
            'Keystone Bank Limited': '082',
            'Mainstreet Bank': '014',
            'Skye Bank': '076',
            'Stanbic IBTC Bank': '221',
            'Standard Chartered Bank': '068',
            'Sterling Bank': '232',
            'Union Bank of Nigeria': '032',
            'United Bank for Africa': '033',
            'Unity Bank': '215',
            'Wema Bank': '035',
            'Zenith Bank': '057',
            'Jaiz Bank': "301",
            'Suntrust Bank': "100",
            "Providus Bank": "101",
            "Parallex Bank": "526",
        }
        return options[bank_name]

def generate_code(referral_class, key='order'):
    def _generate_code():
        t = "ABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(12)])

    code = _generate_code()
    if key == 'slug':
        kwargs = {'slug': code}
    else:
        kwargs = {'order': code}
    while referral_class.objects.filter(**kwargs).exists():
        code = _generate_code()
    return code


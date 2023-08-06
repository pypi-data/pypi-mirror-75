import unittest
import json
import os

import random
import responses

import torchvision
from boris.api import get_presigned_upload_url


class TestGetPresignedURL(unittest.TestCase):

    def setup(self, n_data=1000):

        # set up url
        self.dst_url = os.getenvb(b'BORIS_SERVER_LOCATION',
                                  b'https://api-dev.whattolabel.com').decode()
        self.dataset_id = 'XYZ'
        self.token = 'secret'

        # create a dataset
        self.dataset = torchvision.datasets.FakeData(size=n_data,
                                                     image_size=(3, 32, 32))

    @responses.activate
    def test_signed_url_all_success(self):
        '''Make sure everything works in no-error scenario.

        '''

        self.setup(n_data=10)

        def signed_url_callback(request, psuccess=1.):
            resp_body = {'url': 'https://this-is-a-url.com'}
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps(resp_body))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        for f in self.dataset:
            url, success = get_presigned_upload_url(
                'filename',
                self.dataset_id,
                self.token
            )

    @responses.activate
    def test_signed_url_random_success(self):
        '''Make sure exponential backoff works and we get the url at the end.

        '''

        self.setup(n_data=10)

        def signed_url_callback(request, psuccess=.75):
            resp_body = {'url': 'https://this-is-a-url.com'}
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps(resp_body))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        for f in self.dataset:
            url, success = get_presigned_upload_url(
                'filename',
                self.dataset_id,
                self.token
            )

    @responses.activate
    def test_signed_url_no_success(self):
        """Make sure we get a RuntimeError when we do not receive a url back

        """

        self.setup(n_data=0)

        def signed_url_callback(request, psuccess=0.):
            resp_body = {'url': 'https://this-is-a-url.com'}
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps(resp_body))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        with self.assertRaises(RuntimeError):
            url, success = get_presigned_upload_url(
                'filename',
                self.dataset_id,
                self.token
            )

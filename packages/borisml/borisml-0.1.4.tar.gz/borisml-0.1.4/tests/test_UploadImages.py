import unittest
import json
import os

import random
import responses

import torchvision
import tempfile
import boris.api as api


class TestUploadImages(unittest.TestCase):

    def setup(self, n_data=1000):

        # set up url
        self.dst_url = os.getenvb(b'BORIS_SERVER_LOCATION',
                                  b'https://api-dev.whattolabel.com').decode()
        self.dataset_id = 'XYZ'
        self.token = 'secret'

        # create a dataset
        self.dataset = torchvision.datasets.FakeData(size=n_data,
                                                     image_size=(3, 32, 32))

        self.folder_path = tempfile.mkdtemp()
        sample_names = [f'img_{i}.jpg' for i in range(n_data)]
        for sample_idx in range(n_data):
            data = self.dataset[sample_idx]
            path = os.path.join(self.folder_path, sample_names[sample_idx])
            data[0].save(path)

    @responses.activate
    def test_upload_images_all_success(self):
        """Make sure upload works.

        """

        self.setup(n_data=50)

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

        def put_image_callback(request, psuccess=1.):
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps({}))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.PUT, 'https://this-is-a-url.com',
            callback=put_image_callback,
            content_type='application/json'
        )

        api.upload_images_from_folder(
            self.folder_path,
            dataset_id=self.dataset_id,
            token=self.token
        )

    @responses.activate
    def test_upload_images_random_success(self):
        """Make sure test runs through eventhough not all files get uploaded.

        """

        self.setup(n_data=50)

        def signed_url_callback(request, psuccess=.7):
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

        def put_image_callback(request, psuccess=.7):
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps({}))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.PUT, 'https://this-is-a-url.com',
            callback=put_image_callback,
            content_type='application/json'
        )

        api.upload_images_from_folder(
            self.folder_path,
            dataset_id=self.dataset_id,
            token=self.token
        )

    @responses.activate
    def test_upload_images_no_success(self):
        """Make sure test runs through eventhough not all files get uploaded.

        """

        self.setup(n_data=50)

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

        def put_image_callback(request, psuccess=.0):
            headers = {'request-id': '728d329e-0e86-11e4-a748-0c84dc037c13'}
            if random.random() < psuccess:
                return (200,
                        headers,
                        json.dumps({}))
            else:
                return (500,
                        headers,
                        json.dumps({}))

        responses.add_callback(
            responses.POST, f'{self.dst_url}/getsignedurl',
            callback=signed_url_callback,
            content_type='application/json'
        )

        responses.add_callback(
            responses.PUT, 'https://this-is-a-url.com',
            callback=put_image_callback,
            content_type='application/json'
        )

        with self.assertWarns(Warning):
            api.upload_images_from_folder(
                self.folder_path,
                dataset_id=self.dataset_id,
                token=self.token
            )

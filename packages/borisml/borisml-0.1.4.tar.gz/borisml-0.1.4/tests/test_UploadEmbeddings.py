import unittest
import json
import os

import random
import responses
import numpy as np

import torchvision
import tempfile
from boris.api import upload_embeddings_from_csv
from boris.utils import embeddings_to_pandas


class TestUploadEmbeddings(unittest.TestCase):

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
        self.path_to_embeddings = os.path.join(
            self.folder_path,
            'embeddings.csv')

        sample_names = [f'img_{i}.jpg' for i in range(n_data)]
        labels = [0] * len(sample_names)

        df = embeddings_to_pandas(
            np.random.randn(n_data, 16),
            labels,
            sample_names
        )

        df.to_csv(self.path_to_embeddings)

    @responses.activate
    def test_upload_embeddings_all_success(self):
        """Make sure upload of embeddings works.

        """

        self.setup(n_data=10000)

        def post_embedding_callback(request, psuccess=1.):
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
            responses.POST, f'{self.dst_url}/embeddings',
            callback=post_embedding_callback,
            content_type='application/json'
        )

        success = upload_embeddings_from_csv(
            self.path_to_embeddings,
            dataset_id=self.dataset_id,
            token=self.token
        )

        self.assertTrue(success)

    @responses.activate
    def test_upload_embeddings_random_success(self):
        """Make sure upload of embeddings works.

        """

        self.setup(n_data=5000)

        def post_embedding_callback(request, psuccess=.75):
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
            responses.POST, f'{self.dst_url}/embeddings',
            callback=post_embedding_callback,
            content_type='application/json'
        )

        success = upload_embeddings_from_csv(
            self.path_to_embeddings,
            dataset_id=self.dataset_id,
            token=self.token
        )

        self.assertTrue(success)

    @responses.activate
    def test_upload_embeddings_no_success(self):
        """Make sure upload of embeddings works.

        """

        self.setup(n_data=5000)

        def post_embedding_callback(request, psuccess=.0):
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
            responses.POST, f'{self.dst_url}/embeddings',
            callback=post_embedding_callback,
            content_type='application/json'
        )

        with self.assertRaises(RuntimeError):
            upload_embeddings_from_csv(
                self.path_to_embeddings,
                dataset_id=self.dataset_id,
                token=self.token
            )

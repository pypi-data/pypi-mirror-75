import os
import time
import random
import requests

SERVER_LOCATION = os.getenvb(b'BORIS_SERVER_LOCATION',
                             b'https://api.whattolabel.com').decode()


def _post_request(dst_url, data=None, json=None,
                  max_backoff=32, max_retries=5):

    counter = 0
    backoff = 1. + random.random() * 0.1
    success = False
    while not success:

        response = requests.post(dst_url, data=data, json=json)
        success = (response.status_code == 200)

        # exponential backoff
        if response.status_code in [500, 502]:
            time.sleep(backoff)
            backoff = 2*backoff if backoff < max_backoff else backoff
        # something went wrong
        elif not success:
            msg = f'Failed POST request to {dst_url} with status_code '
            msg += f'{response.status_code}.'
            raise RuntimeError(msg)

        counter += 1
        if counter >= max_retries:
            break

    if not success:
        msg = f'The connection to the server at {dst_url} timed out. '
        raise RuntimeError(msg)

    return response


def _put_request(dst_url, data,
                 max_backoff=32, max_retries=5):

    counter = 0
    backoff = 1. + random.random() * 0.1
    success = False
    while not success:

        response = requests.put(dst_url, data)
        success = (response.status_code == 200)

        # exponential backoff
        if response.status_code in [500, 502]:
            time.sleep(backoff)
            backoff = 2*backoff if backoff < max_backoff else backoff
        # something went wrong
        elif not success:
            msg = f'Failed PUT request to {dst_url} with status_code '
            msg += f'{response.status_code}.'
            raise RuntimeError(msg)

        counter += 1
        if counter >= max_retries:
            break

    if not success:
        msg = f'The connection to the server at {dst_url} timed out. '
        raise RuntimeError(msg)

    return response


def _get_request(dst_url, params=None,
                 max_backoff=32, max_retries=5):

    counter = 0
    backoff = 1. + random.random() * 0.1
    success = False
    while not success:

        response = requests.get(dst_url, params=params)
        success = (response.status_code == 200)

        # exponential backoff
        if response.status_code in [500, 502]:
            time.sleep(backoff)
            backoff = 2*backoff if backoff < max_backoff else backoff
        # something went wrong
        elif not success:
            msg = f'Failed GET request to {dst_url} with status_code '
            msg += f'{response.status_code}.'
            raise RuntimeError(msg)

        counter += 1
        if counter >= max_retries:
            break

    if not success:
        msg = f'The connection to the server at {dst_url} timed out. '
        raise RuntimeError(msg)

    return response


def create_initial_tag(dataset_id: str, token: str):
    """Makes empty post request to dataset to create initial tag

    Args:
        dataset_id: Identifier of the dataset
        token: The token for authenticating the request

    Raises:
        RuntimeError if creation of initial tag failed
    """
    payload = {
        'token': token
    }
    dst_url = f'{SERVER_LOCATION}/users/datasets/{dataset_id}/tags'
    response = _post_request(dst_url, json=payload)
    return response


def get_presigned_upload_url(filename: str,
                             dataset_id: str,
                             token: str) -> str:
    """Creates and returns a signed url to upload an image for a specific dataset

    Args:
        filename: Name of file used for database and cloud storage
        dataset_id: Identifier of the dataset
        token: The token for authenticating the request

    Returns:
        A string containing the signed url

    Raises:
        RuntimeError if requesting signed url failed
    """
    payload = {
        'sample': {
            'fileName': filename,
        },
        'token': token
    }
    dst_url = f'{SERVER_LOCATION}/users/datasets/{dataset_id}/samples'
    response = _post_request(dst_url, json=payload)
    data = response.json()
    signed_url = data['signedWriteUrl']
    return signed_url


def upload_file_with_signed_url(filename: str, url: str) -> bool:
    """Upload a file to the cloud storage using a signed URL

    Args:
        filename: Path to a file for upload
        url: Signed url for push

    Returns:
        A boolean value indicating successful upload
    """
    file = open(filename, 'rb')
    response = _put_request(url, data=file)
    file.close()
    return response


def upload_embedding(data: dict) -> bool:
    """Uploads embedding

    Args:
        data: Object with embedding data

    Returns:
        A boolean value indicating successful upload

    Raises:
        RuntimeError if upload was not successful
    """
    payload = {
        'embeddingName': data['embeddingName'],
        'embeddings': data['embeddings'],
        'token': data['token'],
        'append': data['append'],
    }
    dataset_id = data['datasetId']
    dst_url = f'{SERVER_LOCATION}/users/datasets/{dataset_id}/embeddings'
    response = _post_request(dst_url, json=payload)
    return response


def get_samples(dataset_id: str,
                token: str,
                tag_name: str = 'initial-tag'):
    # payload is the same for both requests
    payload = {
        'token': token
    }

    # get tag_id
    dst_url = f'{SERVER_LOCATION}/users/datasets/{dataset_id}/tags/'
    response = _get_request(dst_url, params=payload)
    tag_ids = [t['_id'] for t in response.json() if t['name'] == tag_name]
    if len(tag_ids) == 0:
        msg = f'No tag with name {tag_name} found '
        msg += f'for datset with id {dataset_id}'
        raise RuntimeError(msg)
    elif len(tag_ids) > 1:
        msg = f'{len(tag_ids)} tags with name {tag_name} founr '
        msg += f'for dataset with id {dataset_id}'
        raise RuntimeError(msg)
    tag_id = tag_ids[0]

    # get files in tag
    dst_url = f'{SERVER_LOCATION}/users/datasets/'
    dst_url += f'{dataset_id}/tags/{tag_id}/download'

    response = _get_request(dst_url, params=payload)
    return response.text.splitlines()

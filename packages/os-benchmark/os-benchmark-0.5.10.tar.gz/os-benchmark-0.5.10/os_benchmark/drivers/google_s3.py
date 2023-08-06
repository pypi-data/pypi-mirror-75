"""
.. note::
  This driver requires `boto3`_.

Configuration
~~~~~~~~~~~~~

.. code-block:: yaml

  ---
  google:
    driver: google_s3
    aws_access_key_id: <_ak>
    aws_secret_access_key: <your_sk>
    project_id: <project_id>

.. _boto3: https://github.com/boto/boto3
"""
from urllib.parse import urljoin
from os_benchmark.drivers import s3


class Driver(s3.Driver):
    """Google Storage S3 Driver"""
    id = 'google_s3'
    endpoint_url = 'https://storage.googleapis.com'
    default_acl = 'public-read-write'
    default_object_acl = 'public-read'
    default_kwargs = {
        'endpoint_url': endpoint_url,
        'region_name': 'auto',
    }

    def _get_create_request_params(self, name, acl, **kwargs):
        params = super()._get_create_request_params(name, acl, **kwargs)
        if self.kwargs['region_name'] != 'auto':
            params['CreateBucketConfiguration'] = {
                'LocationConstraint': self.kwargs['region_name']
            }
        return params

    def get_url(self, bucket_id, name, **kwargs):
        url = urljoin(self.endpoint_url, '%s/%s' % (bucket_id, name))
        return url

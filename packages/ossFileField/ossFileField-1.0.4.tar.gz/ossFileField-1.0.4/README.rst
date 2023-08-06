Django OSS File Field
=========================

**django-oss-file-field** provides a Django Direct File Transfer From Server.


Features
========

- Django Direct File Transfer From Server to OSS
- Flexible File Size/Type Limitation
- Progress Bar Display
- Works in Python 3

Installation
============

* Install

.. code-block:: bash

    $ pip install ossFileField

- Add ``'ossFileField'`` to your ``INSTALLED_APPS`` setting

Authentication settings
=======================

Use the following settings to authenticate with AliCloud OSS.

.. code-block:: bash

    # AliCloud Access Key ID
    OSS_ACCESS_KEY_ID = <Your Access Key ID>

    # AliCloud Access Key Secret
    OSS_ACCESS_KEY_SECRET = <Your Access Key Secret>
    
    # OSS Bucket Name
    OSS_BUCKET_NAME = <Your OSS Bucket name>

    # AliCloud Bucket Host format: http://bucket_name.endpoint eg: http://test.oss-cn-hangzhou.aliyuncs.com
    OSS_BUCKET_HOST = <Your Oss Bucket Host>

    # AliCloud Token Expire Time
    OSS_EXPIRE_TIME = <Token Expire Time>

    # Get OSS Token Routing
    OSS_TOKEN_ROUTE = <Get OSS Token Route>

    # Oss Bucket Proxy URL
    OSS_PROXY_URL = <OSS Bucket Proxy URL>

    # Server URL
    SERVER_URL = <Your App Server Domain URL>

    # Upload To Oss Dir(end of slash)
    UPLOAD_DIR = <Upload OSS Dir>

Get OSS Token
=======================

Register the route in the url file to get the token

.. code-block:: bash

    # urls.py
    from django.conf.urls import url

    from . import views

    urlpatterns = [
        url(r'^get_oss_token$', views.get_oss_token, name='get_oss_token'),
    ]

.. code-block:: bash

    # views.py
    from django.http import HttpResponse
    from django.contrib.auth.decorators import login_required
    from ossFileField.utils import OssToken

    @login_required
    @require_http_methods(["GET"])
    def get_oss_token(request):
        oss_token = OssToken.get_oss_key()
        return HttpResponse(oss_token)

Usage
=======================

models.py import OssFileField

.. code-block:: bash

    # models.py
    from ossFileField import OssFileField


    class Images(models.Model):
        name = models.CharField(max_length=64, blank=False)
        oss_file = OssFileField(prefix='test/', file_type='image', max_file_size='20m', blank=False)

Version
=======================
**1.0.3**
- Support models prefix attribute((end of slash))

- Support limit uploaded file size

- The uploaded file name includes the file origin name and file size

**1.0.4**
- Support public bucket

- Support file name with spaces
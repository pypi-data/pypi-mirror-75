# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function

import errno
import os

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError


class CosClient(object):
    def __init__(self, region, secret_id, secret_key, token=None):
        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token

        if token:
            cos_config = CosConfig(
                Region=region,
                SecretId=secret_id,
                SecretKey=secret_key,
                Token=token,
                Scheme="https",
            )
        else:
            cos_config = CosConfig(
                Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme="https"
            )

        self.client = CosS3Client(cos_config)

    def upload_data(self, path, bucket=None, key_prefix="data", **kwargs):
        """Upload local file or directory to COS.
        """
        # Generate a tuple for each file that we want to upload of the form (local_path, cos_key).
        files = []
        key_suffix = None
        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for name in filenames:
                    local_path = os.path.join(dirpath, name)
                    cos_relative_prefix = (
                        ""
                        if path == dirpath
                        else os.path.relpath(dirpath, start=path) + "/"
                    )
                    cos_prefix = cos_relative_prefix.replace("\\", "/")
                    cos_key = "{}/{}{}".format(key_prefix, cos_prefix, name)
                    files.append((local_path, cos_key))
        else:
            _, name = os.path.split(path)
            cos_key = "{}/{}".format(key_prefix, name)
            files.append((path, cos_key))
            key_suffix = name

        for local_path, cos_key in files:
            self.client.upload_file(
                Bucket=bucket, LocalFilePath=local_path, Key=cos_key, **kwargs
            )

        cos_uri = "cos://{}/{}".format(bucket, key_prefix)
        # If a specific file was used as input (instead of a directory), we return the full cos key
        # of the uploaded object. This prevents unintentionally using other files under the same
        # prefix during training.
        if key_suffix:
            cos_uri = "{}/{}".format(cos_uri, key_suffix)
        return cos_uri

    def download_folder(self, bucket, prefix, download_dir):
        prefix = prefix.lstrip("/")

        marker = ""
        while True:
            response = self.client.list_objects(
                Bucket=bucket, Prefix=prefix, Marker=marker
            )

            for val in response["Contents"]:
                try:
                    cos_relative_path = val["Key"][len(prefix):].lstrip("/")
                    file_path = os.path.join(download_dir, cos_relative_path)
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc:
                    # EEXIST means the folder already exists, this is safe to skip
                    # anything else will be raised.
                    if exc.errno != errno.EEXIST:
                        raise

                response = self.client.get_object(Bucket=bucket, Key=val["Key"])
                response["Body"].get_stream_to_file(file_path)

            if "IsTruncated" not in response:
                break

            if response["IsTruncated"] == "false":
                break

            marker = response["NextMarker"]

    def create_bucket(self, bucket):
        try:
            self.client.create_bucket(Bucket=bucket)
        except CosServiceError as e:
            # print("Default bucket %s is already exists!" % (bucket))
            pass

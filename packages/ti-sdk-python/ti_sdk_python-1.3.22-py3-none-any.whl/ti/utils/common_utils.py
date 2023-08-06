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

from __future__ import absolute_import

import json
import os
import re
import time

import urllib3


def get_temporary_secret_and_token():
    credentials_url = os.environ.get("QCLOUD_CONTAINER_INSTANCE_CREDENTIALS_URL")
    if not credentials_url:
        credentials_url = os.environ.get("INSTANCE_CREDENTIAL_URL")
    if not credentials_url:
        raise AttributeError(
            "Environment error, please provide env {}".format("QCLOUD_CONTAINER_INSTANCE_CREDENTIALS_URL or INSTANCE_CREDENTIAL_URL")
        )

    response = urllib3.PoolManager().request("GET", credentials_url)
    resp_json = json.loads(response.data.decode("utf-8"))
    return (
        resp_json.get("TmpSecretId", None),
        resp_json.get("TmpSecretKey", None),
        resp_json.get("Token", None),
    )


def generate_training_job_name(image):
    m = re.match("^(.+/)?([^:/]+)(:[^:]+)?$", image)
    base_name = m.group(2) if m else image

    timestamp = time.time()
    ms = repr(timestamp).split(".")[1][:3]
    name = time.strftime(
        "%Y-%m-%d-%H-%M-%S-{}".format(ms), time.localtime(timestamp)
    )

    return "{}-{}".format(base_name, name)


def parse_cos_uri(cos_data):
    if not cos_data.startswith("cos://"):
        raise ValueError('COS data uri {} must start with "cos://" '.format(cos_data))

    cos_pattern = re.compile(r"cos://([^/]+)/(.*)")
    cos_match = cos_pattern.match(cos_data)
    bucket_name = cos_match.group(1)
    key_prefix = cos_match.group(2)
    return bucket_name, key_prefix


def command_exists(cmd):
    return any(
        os.access(os.path.join(path, cmd), os.X_OK)
        for path in os.environ["PATH"].split(os.pathsep)
    )

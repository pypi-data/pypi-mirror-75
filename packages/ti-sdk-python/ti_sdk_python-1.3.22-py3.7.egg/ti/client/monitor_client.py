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

import json

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.monitor.v20180724 import monitor_client, models


class MonitorClient(object):
    def __init__(self, region, secret_id, secret_key, token=None):
        cred = credential.Credential(secret_id, secret_key, token)

        http_profile = HttpProfile(endpoint="monitor.tencentcloudapi.com")
        client_profile = ClientProfile(httpProfile=http_profile)
        self._client = monitor_client.MonitorClient(cred, region, client_profile)

    def get_monitor_data(
            self,
            Namespace,
            Instances,
            MetricName,
            StartTime=None,
            EndTime=None,
            Period=None,
    ):
        try:
            request = models.GetMonitorDataRequest()
            params = {
                "Namespace": Namespace,
                "MetricName": MetricName,
                "Instances": Instances,
            }

            if StartTime is not None:
                params["StartTime"] = StartTime

            if EndTime is not None:
                params["EndTime"] = EndTime

            if Period is not None:
                params["Period"] = Period

            print("Monitor request : " + json.dumps(params, indent=2))
            request.from_json_string(json.dumps(params))
            response = self._client.GetMonitorData(request)
            result = json.loads(response.to_json_string())
            print("\nMonitor response : " + json.dumps(result, indent=2))
            return result
        except TencentCloudSDKException as e:
            raise AttributeError(
                "get_monitor_data error, job name: "
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )

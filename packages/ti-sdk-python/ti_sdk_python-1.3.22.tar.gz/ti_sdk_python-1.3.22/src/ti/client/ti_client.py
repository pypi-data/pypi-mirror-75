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
from tencentcloud.tione.v20191022 import tione_client, models

TI_HOST = "tione.tencentcloudapi.com"


class TiClient(object):
    def __init__(self, region, secret_id, secret_key, token=None):
        cred = credential.Credential(secret_id, secret_key, token)

        http_profile = HttpProfile(endpoint=TI_HOST)
        client_profile = ClientProfile(httpProfile=http_profile)
        self._client = tione_client.TioneClient(cred, region, client_profile)

    def create_training_job(
            self,
            TrainingJobName,
            AlgorithmSpecification,
            OutputDataConfig,
            ResourceConfig,
            InputDataConfig=None,
            HyperParameters=None,
            RoleName=None,
            StoppingCondition=None,
            VpcConfig=None,
            EnvConfig=None,
    ):
        try:
            request = models.CreateTrainingJobRequest()
            params = {
                "TrainingJobName": TrainingJobName,
                "AlgorithmSpecification": AlgorithmSpecification,
                "InputDataConfig": InputDataConfig,
                "OutputDataConfig": OutputDataConfig,
                "ResourceConfig": ResourceConfig,
                "RoleName": RoleName,
                "StoppingCondition": StoppingCondition,
            }

            if HyperParameters is not None:
                params["HyperParameters"] = HyperParameters

            if VpcConfig is not None:
                params["VpcConfig"] = VpcConfig

            if EnvConfig is not None:
                params["EnvConfig"] = EnvConfig

            print("Training job request : " + json.dumps(params, indent=2))
            request.from_json_string(json.dumps(params))
            response = self._client.CreateTrainingJob(request)
            result = json.loads(response.to_json_string())
            print("\nTraining job response : " + json.dumps(result, indent=2))
            return result
        except TencentCloudSDKException as e:
            raise AttributeError(
                "Create training job error, job name: "
                + TrainingJobName
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )

    def describe_training_job(self, TrainingJobName):
        try:
            request = models.DescribeTrainingJobRequest()
            params = {
                "TrainingJobName": TrainingJobName,
            }
            request.from_json_string(json.dumps(params))
            # print("Describe Training job request : " + json.dumps(params, indent=2))
            response = self._client.DescribeTrainingJob(request)
            result = json.loads(response.to_json_string())
            # print("\nDescribe Training job response : " + json.dumps(result, indent=2))
            return result
        except TencentCloudSDKException as e:
            print(
                "Describe training job error, job name: "
                + TrainingJobName
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )
            raise AttributeError(
                "Describe training job error, job name: "
                + TrainingJobName
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )

    def stop_training_job(self, TrainingJobName):
        try:
            request = models.StopTrainingJobRequest()
            params = {
                "TrainingJobName": TrainingJobName,
            }
            request.from_json_string(json.dumps(params))
            response = self._client.StopTrainingJob(request)
            # print("Stop training job response: " + response.to_json_string())
            return json.loads(response.to_json_string())
        except TencentCloudSDKException as e:
            print(
                "Stop training job error, job name: "
                + TrainingJobName
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )
            raise AttributeError(
                "Stop training job error, job name: "
                + TrainingJobName
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )

    def describe_training_jobs(self, Filters, Offset, Limit, CreationTimeAfter, CreationTimeBefore):
        try:
            request = models.DescribeTrainingJobsRequest()
            params = {
                "Offset": Offset,
                "Limit": Limit,
            }

            if Filters:
                params["Filters"] = Filters

            if CreationTimeBefore:
                params["CreationTimeBefore"] = CreationTimeBefore

            if CreationTimeAfter:
                params["CreationTimeAfter"] = CreationTimeAfter

            request.from_json_string(json.dumps(params))
            print("Describe Training jobs request : " + json.dumps(params, indent=2))
            response = self._client.DescribeTrainingJobs(request)
            result = json.loads(response.to_json_string())
            print("\nDescribe Training jobs response : " + json.dumps(result, indent=2))
            return result
        except TencentCloudSDKException as e:
            print(
                "Describe training jobs error, job name: "
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )
            raise AttributeError(
                "Describe training jobs error, job name: "
                + ", code: "
                + e.get_code()
                + ", message: "
                + e.get_message()
            )

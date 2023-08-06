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

import json
import sys
import time

from ti.data_source import (
    CosInput,
    FileSystemInput,
    FileSystemOutput,
    FileInput,
)
from ti.utils import parse_cos_uri

class TrainingJob(object):
    """训练任务类

    """

    def __init__(self, estimator):
        self.estimator = estimator

    def train(self, inputs):
        """创建训练任务

        @参数: 
            inputs: (str、FileSystemInput、dict), 表示输入数据源的通道结构。各类型说明如下:
                - str: 存储训练数据集的 COS 路径，如cos://my-bucket/my-training-data。
                - FileSystemInput: 表示 CFS 数据集数据结构，包含文件系统ID、文件系统目录等。
                - dict[str, str]: 指定多个输入数据源通道，例如{'train': 'cos://my-bucket/my-training-data/train', 'test': FileSystemInput}。

        @返回值: 无
        """
        training_channels = None
        if inputs is not None:
            training_channels = self._prepare_input_channels(inputs=inputs)

        output_config = self._prepare_output_config(
            output_path=self.estimator.output_path
        )

        resource_config = self._prepare_resource_config(
            instance_count=self.estimator.train_instance_count,
            instance_type=self.estimator.train_instance_type,
            volume_size=self.estimator.train_volume_size,
        )

        stop_condition = self._prepare_stop_condition(
            max_run=self.estimator.train_max_run
        )
        vpc_config = self._prepare_vpc_config(subnet_id=self.estimator.subnet_id)
        env_config = self._prepare_env_config(envs=self.estimator.envs)

        training_request = {
            "job_name": self.estimator.current_job_name,
            "image_name": self.estimator.image_name,
            "role": self.estimator.role,
            "output_config": output_config,
            "resource_config": resource_config,
            "stop_condition": stop_condition,
        }

        if training_channels and len(training_channels) > 0:
            training_request["input_config"] = training_channels

        if self.estimator.hyperparameters and len(self.estimator.hyperparameters) > 0:
            training_request["hyperparameters"] = json.dumps(
                self.estimator.hyperparameters
            )

        if env_config is not None:
            training_request["env_config"] = env_config

        if vpc_config is not None:
            training_request["vpc_config"] = vpc_config

        self.estimator.ti_session.create_training_job(**training_request)

    def wait(self, wait=True, logs=False):
        """等待训练任务输出信息

        @参数: 
            wait: (bool), 表示是否阻塞直到训练完成。默认为 True，如果设置为 False，fit立即返回，训练任务后台异步执行。

            logs: (bool), 表示是否打印训练任务产生的CLS日志，默认为 False。如果设置为 True，将会从CLS日志获取搜索日志。
            
        @返回值: 无
        """

        if not wait:
            return

        job_name = self.estimator.current_job_name
        cls_client = self.estimator.ti_session.get_cls_client()
        ti_client = self.estimator.ti_session.get_ti_client()

        start_time = time.time()
        end_time = time.time()
        status = "WaitLogging"

        try:
            current_desc = ti_client.describe_training_job(job_name)
        except Exception as e:
            current_desc = {}

        while True:
            if logs and status != "WaitLogging":
                cls_client.flush_log(job_name, start_time, end_time)

            if status == "EndLogging":
                print()
                break

            time.sleep(60)

            # check job state
            pre_desc = current_desc
            try:
                current_desc = ti_client.describe_training_job(job_name)
            except Exception as e:
                current_desc = {}

            if current_desc.get("SecondaryStatus", "") in ("Training", "Completed"):
                status = "StartLogging"

            if current_desc.get("TrainingJobStatus", "") in (
                    "Completed",
                    "Failed",
                    "Stopped",
            ):
                status = "EndLogging"
                # 多睡眠60s，保证log能够上报搭到cls
                time.sleep(60)

            if self._training_status_changed(pre_desc, current_desc):
                print()
                print(self._training_status_message(pre_desc, current_desc), end="")
            else:
                print(".", end="")

            sys.stdout.flush()
            start_time = end_time
            end_time = time.time()

        status = current_desc["TrainingJobStatus"]
        if status not in ("Completed", "Stopped"):
            reason = current_desc.get("FailureReason", "No failure reason")
            raise ValueError(
                "Error for %s. status %s reason: %s" % (job_name, status, reason)
            )

    def _prepare_input_channels(self, inputs):
        input_dict = {}

        if isinstance(inputs, dict):
            for name, input in inputs.items():
                input_dict[name] = self._get_channel_input(input)
        else:
            input_dict["training"] = self._get_channel_input(inputs)

        # input data config convert to channels
        training_channels = []
        for name, input in input_dict.items():
            channel_config = input.config.copy()
            channel_config["ChannelName"] = name

            training_channels.append(channel_config)

        return training_channels

    def _get_channel_input(self, input):
        if isinstance(input, str):
            if input.startswith("cos://"):
                train_input = CosInput(input)
            elif input.startswith("file://"):
                train_input = FileInput(input)
            else:
                raise ValueError(
                    "input {} format error. not in str, dict, CosInput, or FileSystemInput".format(
                        input
                    )
                )

        elif isinstance(input, CosInput):
            train_input = input
        elif isinstance(input, FileSystemInput):
            train_input = input
        else:
            raise ValueError(
                "input {} format error. not in str, dict, CosInput, or FileSystemInput".format(
                    input
                )
            )

        return train_input

    def _prepare_output_config(self, output_path):
        if isinstance(output_path, FileSystemOutput):
            return output_path.config.copy()

        if not output_path.startswith("cos://"):
            return {}

        bucket_name, key_prefix = parse_cos_uri(output_path)
        config = {
            "CosOutputBucket": bucket_name,
            "CosOutputKeyPrefix": key_prefix,
        }

        return config

    def _prepare_resource_config(self, instance_count, instance_type, volume_size):
        return {
            "InstanceCount": instance_count,
            "InstanceType": instance_type,
            "VolumeSizeInGB": volume_size,
        }

    def _prepare_stop_condition(self, max_run):
        return {"MaxRuntimeInSeconds": max_run}

    def _prepare_env_config(self, envs):
        if envs is None or len(envs) == 0:
            return None

        env_config = []
        for k, v in envs.items():
            env_config.append({"Name": k, "Value": v})

        return env_config

    def _prepare_vpc_config(self, subnet_id):
        if subnet_id is None:
            return None

        return {"SubnetId": subnet_id}

    def _training_status_changed(self, pre_desc, current_desc):
        pre_status_transitions = (
            pre_desc.get("SecondaryStatusTransitions", []) if pre_desc else []
        )
        current_status_transitions = (
            current_desc.get("SecondaryStatusTransitions", []) if current_desc else []
        )
        if len(current_status_transitions) == 0:
            return False

        pre_message = (
            pre_status_transitions[-1]["StatusMessage"]
            if len(pre_status_transitions) > 0
            else ""
        )
        current_message = (
            current_status_transitions[-1]["StatusMessage"]
            if len(current_status_transitions) > 0
            else ""
        )

        return pre_message != current_message

    def _training_status_message(self, pre_desc, current_desc):
        pre_status_transitions = (
            pre_desc.get("SecondaryStatusTransitions", []) if pre_desc else []
        )
        current_status_transitions = (
            current_desc.get("SecondaryStatusTransitions", []) if current_desc else []
        )
        if len(current_status_transitions) == 0:
            return ""

        if len(current_status_transitions) == len(pre_status_transitions):
            log_transitions = current_status_transitions[-1:]
        else:
            log_transitions = current_status_transitions[
                              len(pre_status_transitions) - len(current_status_transitions):
                              ]

        statuses = []
        for k in log_transitions:
            statuses.append(
                "{} {} - {}".format(k["StartTime"], k["Status"], k["StatusMessage"])
            )

        return "\n".join(statuses)

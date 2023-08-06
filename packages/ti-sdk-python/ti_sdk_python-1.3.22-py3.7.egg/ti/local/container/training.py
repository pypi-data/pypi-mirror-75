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

from ti.constant import DIR_PARAM_NAME
from ti.data_source import get_file_input
from ti.utils import (
    create_temp_folder,
    write_json_file,
)

from .compose import (
    DockerCompose,
    Volume,
)


class TrainingContainer(object):
    """训练任务容器类

    """

    def __init__(self, ti_session):
        self.ti_session = ti_session

    def train(self, kwargs):
        """创建本地的训练任务

        @参数: 无

        @返回值: 无
        """

        self.root_path = create_temp_folder()
        print(json.dumps(kwargs, indent=4))

        # parse paramters
        job_name = kwargs["TrainingJobName"] if "TrainingJobName" in kwargs else ""
        input_data_config = (
            kwargs["InputDataConfig"] if "InputDataConfig" in kwargs else []
        )
        hyperparameters = (
            kwargs["HyperParameters"] if "HyperParameters" in kwargs else {}
        )
        if isinstance(hyperparameters, str):
            hyperparameters = json.loads(hyperparameters)
            hyperparameters = {
                str(k): json.loads(v) for (k, v) in hyperparameters.items()
            }

        env_configs = (
            kwargs["EnvConfig"] if "EnvConfig" in kwargs and kwargs["EnvConfig"] else []
        )

        instance_count = (
            kwargs["ResourceConfig"]["InstanceCount"]
            if "ResourceConfig" in kwargs
            else 1
        )

        instance_type = (
            kwargs["ResourceConfig"]["InstanceType"]
            if "ResourceConfig" in kwargs
            else "local"
        )

        image = (
            kwargs["AlgorithmSpecification"]["TrainingImageName"]
            if "AlgorithmSpecification" in kwargs
            else 1
        )

        # prepare volumes
        volumes = self._prepare_training_volumes(input_data_config, hyperparameters)

        # generate host config files
        self.hosts = []
        for i in range(instance_count):
            self.hosts.append("{}-{}".format("local-host", i))

        for current_host in self.hosts:
            self._generate_config_files(
                current_host, hyperparameters, input_data_config
            )

        # create envs
        envs = {
            "QCLOUD_REGION": self.ti_session.region_name,
            "TRAINING_JOB_NAME": job_name,
        }

        for v in env_configs:
            envs[v["Name"]] = v["Value"]

        # compose train job
        compose = DockerCompose(image, instance_type, self.root_path, self.hosts)
        compose.generate_compose_command(volumes=volumes, envs=envs, command="train")
        compose.run()

        print("Output model dir: " + self.root_path + "/model/")

    def _prepare_training_volumes(self, input_data_config, hyperparameters):
        volumes = []

        # prepare input channels
        for channel in input_data_config:
            data_source = channel["DataSource"]
            channel_name = channel["ChannelName"]
            file_input = get_file_input(data_source, self.ti_session)

            volumes.append(
                Volume(file_input.get_root_path(), "/opt/ml/input/data/" + channel_name)
            )

        # prepare model path
        volumes.append(Volume(os.path.join(self.root_path, "model"), "/opt/ml/model"))
        volumes.append(
            Volume(os.path.join(self.root_path, "checkpoints"), "/opt/ml/checkpoints")
        )

        # prepare code path
        if DIR_PARAM_NAME in hyperparameters:
            code_path = hyperparameters[DIR_PARAM_NAME]
            volumes.append(Volume(code_path, "/opt/ml/code"))

        return volumes

    def _generate_config_files(self, current_host, hyperparameters, input_data_config):
        for dir in ["input", "input/config", "output"]:
            os.makedirs(os.path.join(self.root_path, current_host, dir))

        config_path = os.path.join(self.root_path, current_host, "input", "config")

        resource_config = {
            "current_host": current_host,
            "hosts": self.hosts,
        }

        channel_configs = {}
        for c in input_data_config:
            channel_name = c["ChannelName"]
            channel_configs[channel_name] = {"TrainingInputMode": "File"}

        write_json_file(
            os.path.join(config_path, "hyperparameters.json"), hyperparameters
        )
        write_json_file(
            os.path.join(config_path, "resourceconfig.json"), resource_config
        )
        write_json_file(
            os.path.join(config_path, "inputdataconfig.json"), channel_configs
        )

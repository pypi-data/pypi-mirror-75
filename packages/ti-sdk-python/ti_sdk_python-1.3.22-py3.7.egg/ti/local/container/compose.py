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

import os
import subprocess
import sys

import yaml


class DockerCompose(object):
    """训练任务编排类

    """

    def __init__(self, image, instance_type, root_path, hosts):
        self.image = image
        self.root_path = root_path
        self.hosts = hosts
        self.instance_type = instance_type

    def generate_compose_command(self, volumes=[], envs={}, command="train"):
        """生成compose文件

        @参数:
            volumes: (list), 表示训练任务的volume列表。

            envs: (list), 表示训练任务的环境变量列表。

            command: (str), 表示容器的脚本执行点

        @返回值: 无
        """

        env_list = []
        for k, v in envs.items():
            env_list.append(k + "=" + v)

        content = {
            "version": "2.3",
            "services": {
                host: self._generate_host_config(host, volumes, env_list, command)
                for host in self.hosts
            },
            "networks": {"ti-network-local": {"name": "ti-network-local"}},
        }

        self.compose_path = os.path.join(
            self.root_path, "ti-" + command + "-compose.yaml"
        )

        content = yaml.dump(content, default_flow_style=False)
        print("docker compose content: \n%s" % content)
        with open(self.compose_path, "w") as f:
            f.write(content)

    def run(self):
        """执行命令

        @参数: 无

        @返回值: 无
        """

        command = [
            "docker-compose",
            "-f",
            self.compose_path,
            "up",
            "--build",
            "--abort-on-container-exit",
        ]

        print("docker compose command: %s" % (" ".join(command)))
        process = subprocess.Popen(command)
        exit_code = process.wait()
        if exit_code != 0:
            raise RuntimeError("Training failed. exited with code: " + exit_code)

    def _generate_host_config(self, host, volumes, envs, command):
        host_volumes = []
        for subdir in ["output", "output/data", "input"]:
            host_dir = os.path.join(self.root_path, host, subdir)
            container_dir = "/opt/ml/{}".format(subdir)
            volume = Volume(host_dir, container_dir)
            host_volumes.append(volume)

        host_volumes.extend(volumes)

        host_config = {
            "image": self.image,
            "stdin_open": True,
            "tty": True,
            "volumes": [
                "{}:{}".format(v.host_dir, v.container_dir) for v in host_volumes
            ],
            "environment": envs,
            "command": command,
            "networks": {"ti-network-local": {"aliases": [host]}},
        }

        if self.instance_type == "local_gpu":
            host_config["runtime"] = "nvidia"

        return host_config


class Volume(object):
    def __init__(self, host_dir, container_dir):
        self.container_dir = container_dir
        self.host_dir = host_dir

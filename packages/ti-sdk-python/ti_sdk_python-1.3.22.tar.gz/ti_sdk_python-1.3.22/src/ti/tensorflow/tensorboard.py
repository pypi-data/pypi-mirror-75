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
import shutil
import subprocess
import threading

from ti.utils import (
    create_temp_folder,
    command_exists,
    parse_cos_uri,
    sync_files,
    get_temporary_secret_and_token,
)


class Tensorboard(threading.Thread):
    """训练任务的Tensorboard类

    """

    def __init__(self, estimator):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.estimator = estimator
        self.tensorboard_tmp_dir = create_temp_folder()
        self.cos_tmp_dir = create_temp_folder()

    def _validate_required_packages(self):
        tensorboard = "tensorboard" if os.name is not "nt" else "tensorboard.exe"
        coscmd = "coscmd" if os.name is not "nt" else "coscmd.exe"

        if not command_exists(tensorboard):
            raise EnvironmentError("EnvironmentError TensorBoard is not installed.")

        if not command_exists(coscmd):
            raise EnvironmentError("EnvironmentError coscmd is not installed.")

    def _start_tensorboard_process(self):
        port = 6006

        for _ in range(100):
            command = [
                "tensorboard",
                "--logdir",
                self.tensorboard_tmp_dir,
                "--host",
                "localhost",
                "--port",
                str(port),
            ]
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            self.event.wait(10)
            if process.poll():
                port += 1
            else:
                return port, process

        raise EnvironmentError("Start TensorBoard fail. No available ports 6000~6099")

    def _init_coscmd_config(self):
        cos_bucket, cos_path = parse_cos_uri(self.estimator.checkpoint_path)

        if self.estimator.ti_session.secret_id:
            secret_id = self.estimator.ti_session.secret_id
            secret_key = self.estimator.ti_session.secret_key
            token = None
        else:
            secret_id, secret_key, token = get_temporary_secret_and_token()

        args = [
            "coscmd",
            "config",
            "-a",
            secret_id,
            "-s",
            secret_key,
            "-r",
            self.estimator.ti_session.region_name,
            "-b",
            cos_bucket,
        ]

        if token:
            args.append("-t")
            args.append(token)

        subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return cos_path

    def run(self):
        """启动Tensorboard实例

        @参数: 无
        
        @返回值: 无
        """

        self._validate_required_packages()

        # start tensorboard process
        port, tensorboard_process = self._start_tensorboard_process()
        print("TensorBoard service port is: %s" % (port))

        # get checkpoint cos url
        while not self.estimator.checkpoint_path:
            self.event.wait(1)
        print(
            "Training job checkpoints cos path: %s" % (self.estimator.checkpoint_path)
        )
        cos_path = self._init_coscmd_config()

        # sync checkpoints
        try:
            while not self.event.is_set():
                args = ["coscmd", "download", cos_path, self.cos_tmp_dir, "-rs"]
                subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                sync_files(self.cos_tmp_dir, self.tensorboard_tmp_dir)
                self.event.wait(10)
        finally:
            shutil.rmtree(self.cos_tmp_dir)
            shutil.rmtree(self.tensorboard_tmp_dir)

        tensorboard_process.terminate()
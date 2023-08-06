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

import logging
import os
import shutil
from packaging import version
from ti.constant import (
    DIR_PARAM_NAME,
    SCRIPT_PARAM_NAME,
    CONTAINER_LOG_LEVEL_PARAM_NAME,
    JOB_NAME_PARAM_NAME,
    TI_REGION_PARAM_NAME,
    TKE_IMAGE_URI,
)
from ti.estimator import EstimatorBase
from ti.utils import (
    create_temp_folder,
    parse_cos_uri,
    file_exist,
    create_tar_file,
)

from ti.data_source import (
    FileSystemOutput,
)

class Framework(EstimatorBase):
    """训练任务的框架基础类，一般不直接调用该类提交任务

    """

    def __init__(
            self,
            entry_point,
            source_dir=None,
            hyperparameters=None,
            envs=None,
            container_log_level=logging.INFO,
            image_name=None,
            **kwargs
    ):
        """初始化Framework实例

        @参数:
            entry_point: (str), 表示训练任务的执行入口点名称。例如下面的代码路径中，mnist.py为训练任务执行入口点，而
                        np_convert.py和image_convert.py分别为依赖的代码。

                ├── code
                │   ├── np_convert.py
                │   ├── image_convert.py
                │   └── mnist.py

            source_dir: (str), 表示训练任务的代码路径。例如下面的代码路径中，code为训练任务的代码路径，将会统一压缩上传到
                        用户训练任务的COS中。

                ├── code
                │   ├── np_convert.py
                │   ├── image_convert.py
                │   └── mnist.py

            hyperparameters: (dict), 表示训练任务的超级参数，将通过config传递到训练容器中。

            envs: (dict), 表示用户自定义的环境变量字典，将传入到训练容器的环境变量里。

            container_log_level: (int), 表示训练时日志打印级别，默认值为INFO。

            image_name: (str), 表示训练任务的镜像，用户可定制传入自己的镜像，需提前存储到TKE的镜像仓库中。

        @返回值: 无
        """

        super(Framework, self).__init__(**kwargs)
        self.entry_point = entry_point
        self.source_dir = source_dir
        self.container_log_level = container_log_level
        self.image_name = image_name

        self.hyperparameters = hyperparameters or {}
        self.envs = envs or {}

    def _prepare_for_training(self, job_name=None):
        if not self.image_name:
            self.image_name = self._get_train_image()

        super(Framework, self)._prepare_for_training(job_name=job_name)

        self._prepare_training_code()

        # update hyperparameters
        self.update_hyperparameters()
        self.hyperparameters[DIR_PARAM_NAME] = self.source_dir
        self.hyperparameters[SCRIPT_PARAM_NAME] = self.entry_point
        self.hyperparameters[CONTAINER_LOG_LEVEL_PARAM_NAME] = self.container_log_level
        self.hyperparameters[JOB_NAME_PARAM_NAME] = self.current_job_name
        self.hyperparameters[TI_REGION_PARAM_NAME] = self.ti_session.region_name

    def _get_image_tag(self):
        if not self.py_version:
            py_version = "py3"
        else:
            py_version = self.py_version

        # new format for high version tensorflow and pytorch
        if self.framework_name == "tensorflow":
            if version.parse(self.framework_version) >= version.parse("2.1"):
                return "{}-gpu-cu101-{}".format(self.framework_version, py_version)
            elif version.parse(self.framework_version) >= version.parse("1.15"):
                return "{}-gpu-cu100-{}".format(self.framework_version, py_version)
        elif self.framework_name == "pytorch":
            if version.parse(self.framework_version) >= version.parse("1.5"):
                return "{}-gpu-cu101-{}".format(self.framework_version, py_version)
            elif version.parse(self.framework_version) >= version.parse("1.3"):
                return "{}-gpu-cu100-{}".format(self.framework_version, py_version)

        # mxnet, sklearn, low version tensorflow and pytorch
        return "{}-{}".format(self.framework_version, py_version)

    def _get_train_image(self):
        image_name = "{}/ti_containers/{}:{}".format(
            TKE_IMAGE_URI, self.framework_name, self._get_image_tag()
        )

        return image_name

    def _prepare_training_code(self):
        if self.entry_point.startswith("cos://"):
            raise ValueError(
                "Invalid entry point: %s. Must be a local file." % self.entry_point
            )

        if self.source_dir and self.source_dir.startswith("cos://"):
            raise ValueError(
                "Invalid source dir: %s. Must be a local dir." % self.source_dir
            )

        if self.source_dir:
            if not file_exist(self.source_dir, self.entry_point):
                raise ValueError(
                    "No file %s was found in directory %s."
                    % (self.entry_point, self.source_dir)
                )

        if not self.ti_session.local_mode:
            if self.source_dir:
                self._upload_training_code()
        else:
            if self.source_dir is None:
                self.source_dir = os.path.dirname(self.entry_point)

            self.source_dir = os.path.abspath(self.source_dir)

    def _upload_training_code(self):
        if isinstance(self.output_path, FileSystemOutput):
            bucket = self.ti_session.default_bucket()
        else:
            bucket, _ = parse_cos_uri(self.output_path)

        prefix = "%s/%s" % (self.current_job_name, "source")

        if self.source_dir is None:
            files = [self.entry_point]
        else:
            files = [
                os.path.join(self.source_dir, name)
                for name in os.listdir(self.source_dir)
            ]

        tmp = create_temp_folder()

        try:
            tar_files = create_tar_file(files, os.path.join(tmp, "source.tar.gz"))
            self.ti_session.upload_data(tar_files, bucket, prefix)
        finally:
            shutil.rmtree(tmp)

        self.source_dir = "cos://%s/%s/source.tar.gz" % (bucket, prefix)

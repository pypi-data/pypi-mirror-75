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
from abc import ABCMeta

from six import with_metaclass
from ti.constant import (
    TRAIN_VOLUME_SIZE,
    TRAIN_MAX_RUN_SECOND,
    DEFAULT_INPUT_MODE,
    TI_ENABLE_CLS_LOG,
)
from ti.local import LocalSession
from ti.session import Session
from ti.train_job import TrainingJob
from ti.utils import generate_training_job_name
from ti.data_source import FileSystemOutput


class EstimatorBase(with_metaclass(ABCMeta, object)):
    """训练任务的EstimatorBase类，框架类、以及自定义Estimator类均从该类继承

    关于TI SDK的介绍请见 https://cloud.tencent.com/document/product/851/40077

    """

    def __init__(
            self,
            role,
            train_instance_count,
            train_instance_type,
            train_volume_size=TRAIN_VOLUME_SIZE,
            train_max_run=TRAIN_MAX_RUN_SECOND,
            input_mode=DEFAULT_INPUT_MODE,
            output_path=None,
            subnet_id=None,
            security_group_ids=None,
            base_job_name=None,
            ti_session=None,
    ):
        """初始化EstimatorBase实例

        @参数:
            role: (str), 表示用户在云控制台创建的角色，需要传递角色给 TI，授权 TI 服务访问用户的云资源。

            train_instance_count: (int), 表示创建的算力实例数量。

            train_instance_type: (str), 表示创建的算力类型，目前支持的类型有。

            train_volume_size: (int), 表示附加的云硬盘大小，单位为GB。

            train_max_run: (int), 表示最大运行时间，单位为秒，超过设定时间若训练未完成，TI 会终止训练任务（默认值: 24 * 60 * 60）。

            input_mode: (str), 表示输入类型，默认值为File。

            base_job_name: (str), 表示指定启动的训练任务名称前缀，如果没有指定，会使用镜像名和时间戳生成默认任务名称。

            output_path: (str), 表示保存模型和输出文件的 COS 路径，如果未指定，会使用默认的存储桶。

            subnet_id: (str), 表示子网ID，如果指定，任务将在有 VPC 配置的情况下训练。

            ti_session: (class type), 表示初始化好的session，当session为空时，将会为EstimatorBase自动创建session。

        @返回值: 无
        """
        self.role = role
        self.train_instance_count = train_instance_count
        self.train_instance_type = train_instance_type
        self.train_volume_size = train_volume_size
        self.train_max_run = train_max_run
        self.input_mode = input_mode
        self.subnet_id = subnet_id
        self.base_job_name = base_job_name
        self.output_path = output_path
        self.checkpoint_path = None

        if self.train_instance_type == "local" or self.train_instance_type == "local_gpu":
            self.ti_session = ti_session or LocalSession()

            if self.train_instance_type == "local_gpu" and self.train_instance_count > 1:
                raise RuntimeError("Distributed Training in Local Gpu is not supported")
        else:
            self.ti_session = ti_session or Session()

    def _prepare_for_training(self, job_name=None):
        if job_name is None:
            if self.base_job_name:
                image_name = self.base_job_name
            else:
                image_name = self.image_name

            job_name = generate_training_job_name(image_name)

        self.current_job_name = job_name

        if self.output_path is None:
            self.output_path = "cos://%s/" % self.ti_session.default_bucket()
        elif isinstance(self.output_path, str) and not self.output_path.endswith("/"):
            self.output_path = self.output_path + "/"

        if isinstance(self.output_path, str) and self.checkpoint_path is None:
            self.checkpoint_path = (
                    self.output_path + self.current_job_name + "/output/checkpoints/"
            )

    def _prepare_for_logs(self, logs=None):
        if logs == False:
            self.hyperparameters[TI_ENABLE_CLS_LOG] = False
        else:
            self.hyperparameters[TI_ENABLE_CLS_LOG] = True

    def fit(self, inputs=None, wait=True, logs=None, job_name=None):
        """提交训练任务

        @参数:
            inputs: (str、FileSystemInput、dict), 表示输入数据源的通道结构。各类型说明如下:
                - str: 存储训练数据集的 COS 路径，如cos://my-bucket/my-training-data。
                - FileSystemInput: 表示 CFS 数据集数据结构，包含文件系统ID、文件系统目录等。
                - dict[str, str]: 指定多个输入数据源通道，例如{'train': 'cos://my-bucket/my-training-data/train', 'test': FileSystemInput}。

            wait: (bool), 表示是否阻塞直到训练完成。默认为 True，如果设置为 False，fit立即返回，训练任务后台异步执行。

            logs: (bool), 表示是否打印训练任务产生的CLS日志，默认为 False。如果设置为 True，将会从CLS日志获取搜索日志。
            
            job_name: (str), 表示训练任务名称。如果未指定，则 Estimator 将根据训练镜像名和时间戳生成默认名字。

        @返回值: 无
        """
        self._prepare_for_logs(logs)
        self._prepare_for_training(job_name)
        self._format_json_hyperparameters_for_training()
        job = TrainingJob(self)
        job.train(inputs)

        if not self.ti_session.local_mode:
            job.wait(wait=wait, logs=logs)

            if isinstance(self.output_path, str) and self.output_path.startswith("cos://"):
                print(
                    "Output uri: "
                    + self.output_path
                    + self.current_job_name
                    + "/output/"
                )
            elif isinstance(self.output_path, FileSystemOutput):
                print(
                    "Output model uri: "
                    + "nfs://"
                    + self.output_path.directory_path()
                    + self.current_job_name+"/"
                )

    def _format_json_hyperparameters_for_training(self):
        self.hyperparameters = {
            str(k): json.dumps(v) for (k, v) in self.hyperparameters.items()
        }


class Estimator(EstimatorBase):
    """训练任务的自定义Estimator类

    关于使用自定义镜像训练模型详情请见 https://cloud.tencent.com/document/product/851/40126

    """

    def __init__(
            self,
            image_name,
            role,
            train_instance_count,
            train_instance_type,
            train_volume_size=TRAIN_VOLUME_SIZE,
            train_max_run=TRAIN_MAX_RUN_SECOND,
            input_mode=DEFAULT_INPUT_MODE,
            output_path=None,
            ti_session=None,
            hyperparameters=None,
            envs=None,
            subnet_id=None,
            security_group_ids=None,
            base_job_name=None,
    ):
        """初始化Estimator实例

        @参数:
            image_name: (str), 表示训练任务的镜像，用户可定制传入自己的镜像，需提前存储到TKE的镜像仓库中。

            role: (str), 表示用户在云控制台创建的角色，需要传递角色给 TI，授权 TI 服务访问用户的云资源。

            train_instance_count: (int), 表示创建的算力实例数量。

            train_instance_type: (str), 表示创建的算力类型，目前支持的类型有。

            train_volume_size: (int), 表示附加的云硬盘大小，单位为GB。

            hyperparameters: (dict), 表示训练任务的超级参数，将通过config传递到训练容器中。

            train_max_run: (int), 表示最大运行时间，单位为秒，超过设定时间若训练未完成，TI 会终止训练任务（默认值: 24 * 60 * 60）。

            input_mode: (str), 表示输入类型，默认值为File。

            base_job_name: (str), 表示指定启动的训练任务名称前缀，如果没有指定，会使用镜像名和时间戳生成默认任务名称。

            output_path: (str), 表示保存模型和输出文件的 COS 路径，如果未指定，会使用默认的存储桶。

            subnet_id: (str), 表示子网ID，如果指定，任务将在有 VPC 配置的情况下训练。

            ti_session: (class type), 表示初始化好的session，当session为空时，将会为EstimatorBase自动创建session。

        @返回值: 无
        """

        super(Estimator, self).__init__(
            role,
            train_instance_count,
            train_instance_type,
            train_volume_size,
            train_max_run,
            input_mode,
            output_path,
            subnet_id,
            security_group_ids,
            base_job_name,
            ti_session,
        )

        self.image_name = image_name
        self.hyperparameters = hyperparameters or {}
        self.envs = envs or {}

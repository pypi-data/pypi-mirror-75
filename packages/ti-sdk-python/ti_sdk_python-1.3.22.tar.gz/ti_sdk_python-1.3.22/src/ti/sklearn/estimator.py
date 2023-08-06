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

from ti.constant import DEFAULT_PY_VERSION
from ti.framework import Framework

DEFAULT_VERSION = "0.20.3"


class SKLearn(Framework):
    """训练任务的SKLearn框架类

    """

    def __init__(
            self, py_version=DEFAULT_PY_VERSION, framework_version=DEFAULT_VERSION, **kwargs
    ):
        """初始化SKLearn实例

        @参数:
            py_version: (str), 表示训练任务的python版本，推荐使用py3，py2后期将不会维护。

            framework_version: (str), 表示训练任务的框架版本，目前SKLearn仅支持0.20.3

        @返回值: 无
        """

        super(SKLearn, self).__init__(**kwargs)

        self.py_version = py_version
        self.framework_version = framework_version
        self.framework_name = "sklearn"

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

        super(SKLearn, self).fit(inputs, wait, logs, job_name)

    def update_hyperparameters(self):
        pass

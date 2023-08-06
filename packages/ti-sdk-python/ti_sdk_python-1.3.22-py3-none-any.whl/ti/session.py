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

import datetime
import os
import time

import pytz
import yaml
from ti.client import (
    TiClient,
    CosClient,
    ClsClient,
    MonitorClient,
)
from ti.utils import get_temporary_secret_and_token

from ti.data_source import FileSystemInput


class Session(object):
    """Session类，腾讯云API访问的统一封装类

    """

    def __init__(self):
        """初始化Session实例，初始化的secret id、secret key将会从~/.ti/config.yaml或临时密钥接口中获取

        @参数: 无

        @返回值: 无
        """

        config_file = os.path.join(os.path.expanduser("~"), ".ti", "config.yaml")
        if os.path.exists(config_file):
            self.config = yaml.load(open(config_file, "r"), Loader=yaml.BaseLoader)
        else:
            raise AttributeError(
                "Config error, please provide the config file: ~/.ti/config.yaml"
            )

        self.region_name = self._get_config_value("basic", "region", "")
        self.app_id = self._get_config_value("basic", "app_id", "")
        self.uin = self._get_config_value("basic", "uin", "")
        self.secret_id = self._get_config_value("basic", "secret_id", "")
        self.secret_key = self._get_config_value("basic", "secret_key", "")
        self.local_mode = False
        self.ti_client = None
        self.cls_client = None
        self.cos_client = None
        self.monitor_client = None

        self._validate_config()

    def _get_config_value(self, group, key, default):
        if group not in self.config:
            return default
        if key not in self.config[group]:
            return default
        return self.config[group][key]

    def _validate_config(self):
        if not self.region_name:
            raise AttributeError(
                "Please provide region name in config file: ~/.ti/config.yaml"
            )
        if not self.uin:
            raise AttributeError("Please provide uin in config file: ~/.ti/config.yaml")
        if not self.app_id:
            raise AttributeError(
                "Please provide appidin config file: ~/.ti/config.yaml"
            )

    def get_ti_client(self):
        if self.local_mode:
            return self.ti_client

        if self.secret_id:
            secret_id, secret_key, token = self.secret_id, self.secret_key, None
        else:
            secret_id, secret_key, token = get_temporary_secret_and_token()

        if secret_id is None:
            return self.ti_client

        self.ti_client = TiClient(self.region_name, secret_id, secret_key, token)
        return self.ti_client

    def get_cls_client(self):
        if self.secret_id:
            secret_id, secret_key, token = self.secret_id, self.secret_key, None
        else:
            secret_id, secret_key, token = get_temporary_secret_and_token()

        if secret_id is None:
            return self.cls_client

        self.cls_client = ClsClient(self.region_name, secret_id, secret_key, token)
        return self.cls_client

    def get_monitor_client(self):
        if self.secret_id:
            secret_id, secret_key, token = self.secret_id, self.secret_key, None
        else:
            secret_id, secret_key, token = get_temporary_secret_and_token()

        if secret_id is None:
            return self.monitor_client

        self.monitor_client = MonitorClient(self.region_name, secret_id, secret_key, token)
        return self.monitor_client

    def get_cos_client(self):
        if self.secret_id:
            secret_id, secret_key, token = self.secret_id, self.secret_key, None
        else:
            secret_id, secret_key, token = get_temporary_secret_and_token()

        if secret_id is None:
            return self.cos_client

        self.cos_client = CosClient(self.region_name, secret_id, secret_key, token)
        return self.cos_client

    def upload_data(self, path, bucket=None, key_prefix="data", **kwargs):
        """上传数据至COS指定路径

        @参数:
            path: (str), 表示上传的本地路径。

            bucket: (str), 表示COS的存储桶。

            key_prefix: (str), 表示COS的目录路径。

        @返回值: (str), 上传成功后的cos uri
        """

        bucket = bucket or self.default_bucket()
        return self.get_cos_client().upload_data(path, bucket, key_prefix, **kwargs)

    def download_folder(self, bucket, prefix, download_dir):
        """下载COS数据至本地路径

        @参数:
            bucket: (str), 表示COS的存储桶。

            prefix: (str), 表示COS的目录路径。

            download_dir: (str), 表示下载的本地路径。

        @返回值: 无
        """

        self.get_cos_client().download_folder(bucket, prefix, download_dir)

    def default_bucket(self):
        """创建COS的默认存储桶

        @参数: 无

        @返回值: (str)，创建的COS的存储桶名称。
        """

        bucket = "ti-{}-{}-{}".format(self.region_name, self.uin, self.app_id)
        self.get_cos_client().create_bucket(bucket)
        return bucket

    def create_training_job(
            self,
            job_name,
            image_name,
            role,
            output_config,
            resource_config,
            stop_condition,
            hyperparameters=None,
            input_config=[],
            env_config=None,
            vpc_config=None,
            input_mode="File",
    ):
        """创建训练任务

        @参数:
            job_name: (str)，表示训练任务名称。

            image_name: (str)，表示训练任务的镜像，用户可定制传入自己的镜像，需提前存储到TKE的镜像仓库中。

            role: (str)，表示用户在云控制台创建的角色，需要传递角色给 TI，授权 TI 服务访问用户的云资源。

            output_config: (dict)，表示训练任务的输出配置，dict示例如下: 
                "OutputDataConfig": {
                    "CosOutputKeyPrefix": "/data",
                    "CosOutputBucket": "test-ap-guangzhou-1233"
                }

            input_config: (dict)，表示训练任务的输入通道配置，dict示例如下: 
                "InputDataConfig": [
                    {
                        "DataSource": {
                            "CosDataSource": {
                            "DataDistributionType": "FullyReplicated",
                            "DataType": "COSPrefix",
                            "Bucket": "test-ap-guangzhou-data",
                            "KeyPrefix": "data/gpu"
                            }
                        },
                        "ChannelName": "train"
                    },
                    {
                        "DataSource": {
                            "FileSystemDataSource": {
                            "FileSystemType": "cfs",
                            "DirectoryPath": "/data/outtt",
                            "FileSystemAccessMode": "rw",
                            "FileSystemId": "cfs-4fjz2tjt"
                            }
                        },
                        "ChannelName": "test"
                    }
                ]

            hyperparameters: (str)，表示训练任务的超级参数，将通过config传递到训练容器中。

            resource_config: (dict)，表示训练任务的资源信息，dict示例如下: 
               "ResourceConfig": {
                    "InstanceType": "TI.SMALL2.1core2g",
                    "VolumeSizeInGB": 0,
                    "InstanceCount": 1
                }

            stop_condition: (dict)，表示训练任务的停止条件，dict示例如下: 
                "StoppingCondition": {
                    "MaxRuntimeInSeconds": 86400
                }

            env_config: (dict)，表示训练任务的环境变量信息，dict示例如下: 
                "EnvConfig":[
                    {
                        "Name" : "GPU_NUM",
                        "Value" : "2"
                    },
                    {
                        "Name" : "CPU_NUM",
                        "Value" : "24"	
                    }
                ]

            vpc_config: (dict)，表示训练任务的私有网络信息，dict示例如下: 
                "VpcConfig": {
                    "SubnetId": "subnet-xxxyyy"
                }

            input_mode: 表示输入类型，默认 File。

        @返回值: (dict)，创建的训练任务信息，主要包括任务名称
        """

        training_request = {
            "AlgorithmSpecification": {
                "TrainingInputMode": input_mode,
                "TrainingImageName": image_name,
            },
            "TrainingJobName": job_name,
            "RoleName": role,
            "StoppingCondition": stop_condition,
            "ResourceConfig": resource_config,
            "OutputDataConfig": output_config,
            "InputDataConfig": input_config,
            "HyperParameters": hyperparameters,
            "VpcConfig": vpc_config,
            "EnvConfig": env_config,
        }

        self.get_ti_client().create_training_job(**training_request)

    def stop_training_job(self, job_name):
        """停止训练任务

        @参数:
            job_name: (str), 表示训练任务名称

        @返回值: 无
        """

        self.get_ti_client().stop_training_job(TrainingJobName=job_name)

    def describe_training_job(self, job_name):
        """查询训练任务信息

        @参数:
            job_name: (str), 表示训练任务名称

        @返回值: (dict)，训练任务的详细信息，格式如下
                {
                  "AlgorithmSpecification": {
                    "TrainingImageName": "ccr.ccs.tencentyun.com/ti_public/tensorflow:1.14.0-py3",
                    "TrainingInputMode": "File",
                    "AlgorithmName": null
                  },
                  "TrainingJobName": "tensorflow-111-05-22-07-1-1-1",
                  "HyperParameters": "{\"ti_submit_directory\":\"\\\"cos://ti-ap-guangzhou-111-22/tensorflow-2020-05-22-07-00-35-491/source/source.tar.gz\\\"\",\"ti_program\":\"\\\"tf_mnist.py\\\"\"}",
                  "InputDataConfig": [
                    {
                      "ChannelName": "training",
                      "DataSource": {
                        "CosDataSource": {
                          "Bucket": "ti-ap-guangzhou-111-22",
                          "KeyPrefix": "train-data/test",
                          "DataDistributionType": "FullyReplicated",
                          "DataType": "COSPrefix"
                        },
                        "FileSystemDataSource": null
                      },
                      "InputMode": null,
                      "ContentType": null
                    }
                  ],
                  "OutputDataConfig": {
                    "CosOutputBucket": "ti-ap-guangzhou-111-22",
                    "CosOutputKeyPrefix": "",
                    "FileSystemOutputPath": null
                  },
                  "StoppingCondition": {
                    "MaxRuntimeInSeconds": 86400
                  },
                  "ResourceConfig": {
                    "InstanceCount": 1,
                    "InstanceType": "TI.MEDIUM4.2core4g",
                    "VolumeSizeInGB": 0
                  },
                  "VpcConfig": null,
                  "InstanceId": "timaker-xxxxx",
                  "FailureReason": null,
                  "LastModifiedTime": "2020-05-22 16:12:44",
                  "TrainingStartTime": "2020-05-22 16:12:22",
                  "TrainingEndTime": "2020-05-22 16:12:45",
                  "ModelArtifacts": {
                    "CosModelArtifacts": "https://console.cloud.tencent.com/cos5/bucket/setting?type=objectDetail&bucketName=ti-ap-guangzhou-111-22&path=/tensorflow-2020-05-22-07-00-35-491/output/model.tar.gz&region=ap-guangzhou"
                  },
                  "SecondaryStatus": "Completed",
                  "SecondaryStatusTransitions": [
                    {
                      "StartTime": "2020-05-22 15:00:41",
                      "EndTime": "2020-05-22 15:02:56",
                      "Status": "Starting",
                      "StatusMessage": "Launching ML instance"
                    },
                    {
                      "StartTime": "2020-05-22 15:02:56",
                      "EndTime": "2020-05-22 15:02:57",
                      "Status": "Starting",
                      "StatusMessage": "ML instance ready"
                    },
                    {
                      "StartTime": "2020-05-22 15:02:57",
                      "EndTime": "2020-05-22 15:04:15",
                      "Status": "Downloading",
                      "StatusMessage": "Downloading training data"
                    },
                    {
                      "StartTime": "2020-05-22 15:04:15",
                      "EndTime": "2020-05-22 15:04:18",
                      "Status": "Downloading",
                      "StatusMessage": "Training data ready"
                    },
                    {
                      "StartTime": "2020-05-22 15:04:18",
                      "EndTime": "2020-05-22 16:12:22",
                      "Status": "Training",
                      "StatusMessage": "Starting train job"
                    },
                    {
                      "StartTime": "2020-05-22 16:12:22",
                      "EndTime": "2020-05-22 16:12:23",
                      "Status": "Training",
                      "StatusMessage": "Training finished"
                    },
                    {
                      "StartTime": "2020-05-22 16:12:23",
                      "EndTime": "2020-05-22 16:12:45",
                      "Status": "Uploading",
                      "StatusMessage": "Uploading job output"
                    },
                    {
                      "StartTime": "2020-05-22 16:12:45",
                      "EndTime": null,
                      "Status": "Completed",
                      "StatusMessage": "Training Job completed"
                    }
                  ],
                  "RoleName": "TIONE_QCSRole",
                  "TrainingJobStatus": "Completed",
                }

        """

        return self.get_ti_client().describe_training_job(TrainingJobName=job_name)

    def describe_training_jobs(self, filters=[], offset=0, limit=20, creation_time_after=None,
                               creation_time_before=None):
        """查询训练任务列表信息

        @参数:
            filters: (list)，表示训练任务的过滤条件，dict示例如下:
                    [
                        {
                            "Name": "instance-name",
                            "Values": ["tensorflow-1"],
                        },
                        {
                            "Name": "search-by-name",
                            "Values": ["tensorflow"],
                        },
                        {
                            "Name": "status",
                            "Values": ["Completed", "Stopped"],
                        }
                    ]

            其中，instance-name按照名称过滤，search-by-name按照名称检索，模糊匹配，
                status按照状态来检索，状态值包括Completed、Failed、、Stopped、InProgress

            offset: (str), 表示偏移量

            limit: (str), 表示限制数目

            creation_time_before: (str)，表示训练任务创建时间早于的时间点，如2020-05-22 17:51:00

            creation_time_after: (str)，表示训练任务创建时间晚于的时间点，如2020-05-22 17:51:00

        @返回值: (dict)，训练任务的列表信息，格式如下：
                {
                  "TrainingJobSet": [
                    {
                      "CreationTime": "2020-05-22 15:00:36",
                      "LastModifiedTime": "2020-05-22 16:12:44",
                      "TrainingJobName": "tensorflow-1111-22-22-07-11-35-11",
                      "TrainingJobStatus": "Completed",
                      "TrainingEndTime": "2020-05-22 16:12:45",
                      "InstanceId": "timaker-xxxxx",
                      "ResourceConfig": {
                        "InstanceCount": 1,
                        "InstanceType": "TI.MEDIUM4.2core4g",
                        "VolumeSizeInGB": 0
                      }
                    },
                    {
                      "CreationTime": "2020-05-22 15:00:04",
                      "LastModifiedTime": "2020-05-22 15:14:02",
                      "TrainingJobName": "tensorflow-2020-05-22-07-00-04-038",
                      "TrainingJobStatus": "Completed",
                      "TrainingEndTime": "2020-05-22 15:14:02",
                      "InstanceId": "timaker-yyyyy",
                      "ResourceConfig": {
                        "InstanceCount": 1,
                        "InstanceType": "TI.SMALL2.1core2g",
                        "VolumeSizeInGB": 0
                      }
                    },
                    {
                      "CreationTime": "2020-05-20 13:04:09",
                      "LastModifiedTime": "2020-05-20 13:16:01",
                      "TrainingJobName": "tensorflow-2020-09-21-22-09-08-11",
                      "TrainingJobStatus": "Completed",
                      "TrainingEndTime": "2020-05-20 13:16:02",
                      "InstanceId": "timaker-yyyyyy",
                      "ResourceConfig": {
                        "InstanceCount": 1,
                        "InstanceType": "TI.SMALL2.1core2g",
                        "VolumeSizeInGB": 0
                      }
                    }
                  ],
                  "TotalCount": 11,
                }
        """

        return self.get_ti_client().describe_training_jobs(filters, offset, limit, creation_time_after,
                                                           creation_time_before)

    def get_monitor_data(self, job_name, metric_name, start_time=None,
                         end_time=None, period=None):
        """查询训练任务指标监控信息

        @参数:
            job_name: (str), 表示训练任务名称

            metric_name: (str)，表示训练任务的监控指标名称，取值为CpuCoreUsed、CpuCoreUsedRate、MemUsage、
                        MemUsageRate、GpuCoreUsed、GpuCoreUsedRate

            start_time: (str)，表示起始时间，如2020-05-22 17:51:00

            end_time: (str)，表示结束时间，如2020-05-23 17:51:00

            period: (int), 表示监控统计周期。默认为取值为300，单位为s。取值为60、300等

        @返回值: (dict)，训练任务的监控信息，格式如下：
                {
                  "Period": 300,
                  "MetricName": "CpuCoreUsedRate",
                  "DataPoints": [
                    {
                      "Dimensions": [
                        {
                          "Name": "JobId",
                          "Value": "timaker-xxxxx"
                        }
                      ],
                      "Timestamps": [
                        1593585600,
                        1593585900
                      ],
                      "Values": [
                        0,
                        0.47
                      ]
                    }
                  ],
                  "StartTime": "2020-07-01 11:40:00",
                  "EndTime": "2020-07-01 17:50:00",
                  "RequestId": "4d7a04c2-b847-4b21-8fe8-63bca569b846"
                }
        """

        res = self.describe_training_job(job_name)
        instance_id = res.get("InstanceId", None)
        if instance_id is None:
            raise RuntimeError("get monitor data failed. training job can not find instanceId")

        dimensions = {
            "Dimensions": [
                {
                    "Name": "JobId",
                    "Value": instance_id
                }
            ]
        }

        namespace = "qce/tione_sdk_job"

        return self.get_monitor_client().get_monitor_data(namespace, [dimensions], metric_name, start_time, end_time,
                                                          period)

    def search_log(self, job_name, start_time=None, end_time=None, limit=100, context=""):
        """查询训练任务列表信息

        @参数:
            job_name: (str), 表示训练任务名称

            start_time: (str)，表示起始时间，如2020-05-22 17:51:00

            end_time: (str)，表示结束时间，如2020-05-23 17:51:00

            limit: (int), 表示单次要返回的日志条数，单次返回的最大条数为100

            context: (str)，表示加载更多使用，透传上次返回的 context 值，获取后续的日志内容，通过游标最多可获取10000条，请尽可能缩小时间范围

        @返回值: (dict)，训练任务的日志信息
            context: (str)，表示获取更多检索结果的游标

            listover: (bool)，表示搜索结果是否已经全部返回

            results: (list)，表示日志内容信息

            日志返回内容如下：
                {
                  "context": "xxxxxyyyyyyyyy",
                  "listover": false,
                  "results": [
                    {
                      "content": "{\"job\":\"tensorflow-11\",\"message\":\"INFO - root - starting dd task\\n\",\"stream\":\"stderr\"}\n",
                      "filename": "",
                      "source": "",
                      "timestamp": "2020-07-02 11:24:50",
                      "topic_id": "bb-aa-dd-ee-cc",
                      "topic_name": "TrainingJob"
                    },
                    {
                      "content": "{\"job\":\"tensorflow-11\",\"message\":\"INFO - root - running entrypoint\\n\",\"stream\":\"stderr\"}\n",
                      "filename": "",
                      "source": "",
                      "timestamp": "2020-07-02 11:24:50",
                      "topic_id": "bb-aa-dd-ee-cc",
                      "topic_name": "TrainingJob"
                    }
                  ],
                  "sql_flag": false
                }
        """

        if start_time is None:
            start_time = datetime.datetime.fromtimestamp(
                int(time.time()) - 3600, pytz.timezone("Asia/Shanghai")
            ).strftime("%Y-%m-%d %H:%M:%S")

        if end_time is None:
            end_time = datetime.datetime.fromtimestamp(
                int(time.time()), pytz.timezone("Asia/Shanghai")
            ).strftime("%Y-%m-%d %H:%M:%S")

        return self.get_cls_client().search_log(job_name, start_time, end_time, limit, context)

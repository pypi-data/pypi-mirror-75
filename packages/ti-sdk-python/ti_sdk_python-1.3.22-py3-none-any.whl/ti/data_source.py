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

import os

from six.moves.urllib.parse import urlparse
from ti.utils import (
    parse_cos_uri,
    create_temp_folder,
)


class CosInput(object):
    """COS输入数据源数据结构

    """

    def __init__(
            self, cos_data, distribution="FullyReplicated", cos_data_type="COSPrefix",
    ):
        """COS输入数据源

        @参数:
            cos_data: (str), 表示COS的URI。

            distribution: (str), 表示COS的数据分布类型。

            cos_data_type: (str), 表示COS的数据类型。

        @返回值: 无
        """

        bucket, key_prefix = parse_cos_uri(cos_data)

        self.config = {
            "DataSource": {
                "CosDataSource": {
                    "DataDistributionType": distribution,
                    "DataType": cos_data_type,
                    "Bucket": bucket,
                    "KeyPrefix": key_prefix,
                }
            }
        }


class FileSystemInput(object):
    """文件系统输入数据源数据结构

    """

    def __init__(
            self, file_system_id, directory_path, file_system_type, file_system_access_mode
    ):
        """文件系统输入数据源

        @参数:
            file_system_id: (str), 表示文件系统ID。

            directory_path: (str), 表示文件系统的挂载目录。

            file_system_type: (str), 表示文件系统类型，目前仅支持CFS。

            file_system_access_mode: (str), 表示文件系统的访问模式，目前为rw和ro。

        @返回值: 无
        """

        self.config = {
            "DataSource": {
                "FileSystemDataSource": {
                    "FileSystemId": file_system_id,
                    "FileSystemType": file_system_type,
                    "DirectoryPath": directory_path,
                    "FileSystemAccessMode": file_system_access_mode,
                }
            }
        }


class FileSystemOutput(object):
    """文件系统输出数据源数据结构

    """

    def __init__(
            self, file_system_id, directory_path, file_system_type
    ):
        """文件系统输出数据源

        @参数:
            file_system_id: (str), 表示文件系统ID。

            directory_path: (str), 表示文件系统的挂载目录。

            file_system_type: (str), 表示文件系统类型，目前仅支持CFS。

        @返回值: 无
        """

        self.config = {
            "FileSystemDataSource": {
                "FileSystemId": file_system_id,
                "FileSystemType": file_system_type,
                "DirectoryPath": directory_path,
                "FileSystemAccessMode": "rw",
            }
        }


class FileInput(object):
    """文件输入数据源数据结构

    """

    def __init__(self, file_uri):
        """文件系统输入数据源

        @参数:
            file_uri: (str), 表示文件的URI。

        @返回值: 无
        """

        self.config = {"DataSource": {"FileDataSource": {"FileUri": file_uri, }}}

        parsed_uri = urlparse(file_uri)
        self.file_path = parsed_uri.netloc + parsed_uri.path

    def get_root_path(self):
        if os.path.isdir(self.file_path):
            return self.file_path
        return os.path.dirname(self.file_path)


def get_file_input(data_source, ti_session):
    """获取文件输入数据源数据结构

    @参数:
        data_source: (dict), 表示源输入数据源格式。

        ti_session: (class type), 表示初始化好的ti session。

    @返回值: (FileInput), 文件输入数据源
    """

    if "FileDataSource" in data_source:
        return FileInput(data_source["FileDataSource"]["FileUri"])
    elif "CosDataSource" in data_source:
        download_dir = create_temp_folder()
        ti_session.download_folder(
            bucket=data_source["CosDataSource"]["Bucket"],
            prefix=data_source["CosDataSource"]["KeyPrefix"],
            download_dir=download_dir,
        )

        return FileInput("file://" + download_dir)
    else:
        raise ValueError(
            "DataSource should be File or COS. DataSource: {}".format(data_source)
        )

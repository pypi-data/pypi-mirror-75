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
import platform
import tarfile
import tempfile


def create_temp_folder():
    working_dir = tempfile.mkdtemp()
    if platform.system() == "Darwin":
        working_dir = "/private{}".format(working_dir)

    return os.path.abspath(working_dir)


def write_json_file(name, content):
    with open(name, "w") as f:
        json.dump(content, f)


def file_exist(directory, name):
    if not os.path.isfile(os.path.join(directory, name)):
        return False

    return True


def create_tar_file(files, target):
    with tarfile.open(target, mode="w:gz") as t:
        for f in files:
            t.add(f, arcname=os.path.basename(f))

    return target


def sync_files(src_dir, dist_dir):
    for src_path, dirs, files in os.walk(src_dir):
        dist_path = src_path.replace(src_dir, dist_dir)

        for name in dirs:
            dir = os.path.join(dist_path, name)
            if not os.path.exists(dir):
                os.mkdir(dir)

        for name in files:
            src_file = os.path.join(src_path, name)
            dist_file = os.path.join(dist_path, name)
            with open(src_file, "rb") as a, open(dist_file, "wb") as b:
                b.write(a.read())

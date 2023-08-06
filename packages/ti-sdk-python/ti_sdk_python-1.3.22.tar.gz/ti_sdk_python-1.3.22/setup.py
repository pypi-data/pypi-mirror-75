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

from setuptools import setup, find_packages


def requirements():
    with open('requirements.txt', 'r') as fileobj:
        requirements = [line.strip() for line in fileobj]
        return requirements


def read(fname):
    with open(fname, 'r', encoding="utf-8") as file:
        return file.read()


setup(
    name="ti_sdk_python",
    version=read("version").strip(),
    url='https://cloud.tencent.com',
    license="Apache License 2.0",
    description="Open source library for training and deploying models on TencentCloud TIONE.",
    long_description=read("README.md"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires='>=3',
    install_requires=requirements(),
    long_description_content_type='text/markdown',
    author="TencentCloud TIONE",
    keywords="TencentCloud ML TI AI Training",
)

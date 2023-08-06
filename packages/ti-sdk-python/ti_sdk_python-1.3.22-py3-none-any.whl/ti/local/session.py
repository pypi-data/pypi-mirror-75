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

from ti.local.container import TrainingContainer
from ti.session import Session


class LocalSession(Session):
    """训练任务的local session

    """

    def __init__(self):
        super(LocalSession, self).__init__()
        self.ti_client = LocalClient(self)
        self.local_mode = True


class LocalClient(object):
    """训练任务的local client

    """

    def __init__(self, ti_session):
        self.ti_session = ti_session

    def create_training_job(self, **kwargs):
        print("start local training job")
        TrainingContainer(self.ti_session).train(kwargs)
        print("local training job completed")

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

SCRIPT_PARAM_NAME = "ti_program"
DIR_PARAM_NAME = "ti_submit_directory"
CONTAINER_LOG_LEVEL_PARAM_NAME = "ti_container_log_level"
JOB_NAME_PARAM_NAME = "ti_job_name"
TI_REGION_PARAM_NAME = "ti_region"

TI_ENABLE_CLS_LOG = "ti_enable_cls_log"

LAUNCH_PS_ENV_NAME = "ti_parameter_server_enabled"
LAUNCH_MPI_ENV_NAME = "ti_mpi_enabled"
MPI_NUM_PROCESSES_PER_HOST = "ti_mpi_num_of_processes_per_host"
MPI_CUSTOM_MPI_OPTIONS = "ti_mpi_custom_mpi_options"

TKE_IMAGE_URI = "ccr.ccs.tencentyun.com"

TRAIN_MAX_RUN_SECOND = 24 * 60 * 60
TRAIN_VOLUME_SIZE = 0
DEFAULT_INPUT_MODE = "File"
DEFAULT_PY_VERSION = "py3"

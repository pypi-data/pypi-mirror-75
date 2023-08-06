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

import datetime
import hashlib
import hmac
import http.client
import json
import time
import os

import pytz
from six.moves.urllib.parse import quote, urlencode

CLS_HOST = "%s.cls.tencentcs.com"


class ClsClient(object):
    def __init__(self, region, secret_id, secret_key, token=None):
        self.region = region
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token
        self.logset_id = None
        self.topic_id = None
        self.host = CLS_HOST % (self.region)

    def send_request(self, action, params):
        sign = signature(
            secret_id=self.secret_id,
            secret_key=self.secret_key,
            method="GET",
            path="/" + action,
            params=params,
            headers={"Host": self.host, "User-Agent": "AuthSDK"},
            expire=300,
        )

        paramStr = ""
        for key, value in params.items():
            if len(paramStr) > 0:
                paramStr = paramStr + "&" + key + "=" + quote(str(value))
            else:
                paramStr = paramStr + key + "=" + quote(str(value))

        url = "http://%s/%s?%s" % (self.host, action, paramStr)

        http_proxy_host = os.environ.get("HTTP_PROXY_HOST", None)
        http_proxy_port = os.environ.get("HTTP_PROXY_PORT", 80)

        if http_proxy_host:
            conn = http.client.HTTPConnection(http_proxy_host, http_proxy_port)
        else:
            conn = http.client.HTTPConnection(self.host)

        headers = {"Host": self.host, "Authorization": sign}

        if self.token:
            headers["x-cls-Token"] = self.token

        try:
            conn.request("GET", url, None, headers)
            res = conn.getresponse()

            resp = json.loads(res.read())

            if "errorcode" in resp or "errormessage" in resp:
                print(
                    "cls errorcode : %s errormessage: %s"
                    % (resp["errorcode"], resp["errormessage"])
                )
                return -1, resp["errormessage"], {}

            return 0, "ok", resp
        except Exception as e:
            print(
                "cls send fail, exception: [%s]",
                e,
            )
            return -1, e, {}

    def query_logsets(self):
        if self.logset_id:
            return

        params = {}
        code, msg, data = self.send_request("logsets", params)
        if code != 0:
            return

        # print(data)
        for val in data.get("logsets", []):
            if val["logset_name"] == "TiOne":
                self.logset_id = val["logset_id"]

    def query_topics(self):
        if self.topic_id:
            return

        if self.logset_id is None:
            return

        params = {"logset_id": self.logset_id}
        code, msg, data = self.send_request("topics", params)
        if code != 0:
            return
        # print(data)
        for val in data.get("topics", []):
            if val["topic_name"] == "TrainingJob":
                self.topic_id = val["topic_id"]

    def search_log(self, job_name, start_time, end_time, limit, context):
        self.query_logsets()
        self.query_topics()

        if self.topic_id is None:
            return

        if self.logset_id is None:
            return

        params = {
            "logset_id": self.logset_id,
            "topic_ids": self.topic_id,
            "query": "job:" + job_name,
            "limit": limit,
            "sort": "asc",
            "start_time": start_time,
            "end_time": end_time,
        }

        if context:
            params["context"] = context

        try:
            print("CLS log request : " + json.dumps(params, indent=2))
            code, msg, data = self.send_request("searchlog", params)
            print("\nCLS log response : " + json.dumps(data, indent=2))
            return data
        except Exception as e:
            raise AttributeError(
                "search_log error, job name: "
                + ", message: "
                + msg
            )

    def flush_log(self, job_name, start_time, end_time):
        self.query_logsets()
        self.query_topics()

        if self.topic_id is None:
            return

        if self.logset_id is None:
            return

        start_time = datetime.datetime.fromtimestamp(
            int(start_time), pytz.timezone("Asia/Shanghai")
        ).strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.fromtimestamp(
            int(end_time), pytz.timezone("Asia/Shanghai")
        ).strftime("%Y-%m-%d %H:%M:%S")

        # print("start_time %s" % start_time)
        # print("end_time %s" % end_time)

        context = ""

        while True:
            params = {
                "logset_id": self.logset_id,
                "topic_ids": self.topic_id,
                "query": "job:" + job_name,
                "limit": 100,
                "sort": "asc",
                "start_time": start_time,
                "end_time": end_time,
                "context": context,
            }

            code, msg, data = self.send_request("searchlog", params)
            for val in data.get("results", []):
                # print("%s-%s" % (val["timestamp"], json.loads(val["content"])["message"]), end='')
                try:
                    ct = json.loads(val["content"])
                    if ct.get("message"):
                        print(ct["message"], end="")
                    elif ct.get("log"):
                        print(ct["log"], end="")
                except Exception as e:
                    pass

            context = data.get("context", "")
            if context == "":
                break


def signature(
        secret_id, secret_key, method="GET", path="/", params={}, headers={}, expire=120
):
    # reserved keywords in headers urlencode are -_.~, notice that / should be encoded and space should not be encoded to plus sign(+)
    filt_headers = dict(
        (k.lower(), quote(headers[k].encode("utf-8"), "-_.~"))
        for k in headers
        if k.lower() == "content-type"
        or k.lower() == "content-md5"
        or k.lower() == "host"
        or k[0].lower() == "x"
    )
    uri_params = dict((k.lower(), params[k]) for k in params)
    format_str = u"{method}\n{host}\n{params}\n{headers}\n".format(
        method=method.lower(),
        host=path,
        params=urlencode(sorted(uri_params.items()))
            .replace("+", "%20")
            .replace("%7E", "~"),
        headers="&".join(
            map(lambda tupl: "%s=%s" % (tupl[0], tupl[1]), sorted(filt_headers.items()))
        ),
    )
    start_sign_time = int(time.time())
    sign_time = "{bg_time};{ed_time}".format(
        bg_time=start_sign_time - 60, ed_time=start_sign_time + expire
    )
    # sign_time = "1510109254;1510109314"
    sha1 = hashlib.sha1()
    sha1.update(format_str.encode("utf-8"))

    str_to_sign = "sha1\n{time}\n{sha1}\n".format(time=sign_time, sha1=sha1.hexdigest())
    sign_key = hmac.new(
        secret_key.encode("utf-8"), sign_time.encode("utf-8"), hashlib.sha1
    ).hexdigest()
    sign = hmac.new(
        sign_key.encode("utf-8"), str_to_sign.encode("utf-8"), hashlib.sha1
    ).hexdigest()
    sign_tpl = "q-sign-algorithm=sha1&q-ak={ak}&q-sign-time={sign_time}&q-key-time={key_time}&q-header-list={headers}&q-url-param-list={params}&q-signature={sign}"

    return sign_tpl.format(
        ak=secret_id,
        sign_time=sign_time,
        key_time=sign_time,
        params=";".join(sorted(map(lambda k: k.lower(), uri_params.keys()))),
        headers=";".join(sorted(filt_headers.keys())),
        sign=sign,
    )

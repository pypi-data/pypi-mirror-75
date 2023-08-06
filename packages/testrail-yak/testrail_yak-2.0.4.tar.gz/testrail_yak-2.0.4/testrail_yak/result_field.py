#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class ResultField(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get(self) -> list:
        try:
            result = self.client.send_get("get_result_fields")
        except APIError as error:
            print(error)
            raise ResultFieldException
        else:
            return result


class ResultFieldException(Exception):
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class Priority(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_priorities(self) -> list:
        try:
            result = self.client.send_get("get_priorities")
        except APIError as error:
            print(error)
            raise PriorityException
        else:
            return result


class PriorityException(Exception):
    pass

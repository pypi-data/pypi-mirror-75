#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import CaseFieldSchema, SchemaError
import json


class CaseField(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_case_fields(self) -> list:
        """Returns a list of available test case custom fields. """
        try:
            result = self.client.send_get(f"get_case_fields")
        except APIError as error:
            print(error)
            raise CaseFieldException
        else:
            # not sure this is needed, added it to help debug
            if type(result) == str:
                result = json.loads(fr"{result}")
            return result

    def add_case_field(self, data: dict) -> dict:
        """Creates a new test case custom field. """

        try:
            data = CaseFieldSchema(partial=True).load(data)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_case_field", data=data)
            except APIError as error:
                print(error)
                raise CaseFieldException
            else:
                # not sure this is needed, added it to help debug
                if type(result) == str:
                    result = json.loads(fr"{result}")
                return result


class CaseFieldException(Exception):
    pass

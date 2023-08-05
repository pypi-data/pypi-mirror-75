#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class Template(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_templates(self, project_id: int) -> list:
        """Returns a list of available templates. """
        try:
            result = self.client.send_get(f"get_templates/{project_id}")
        except APIError as error:
            print(error)
            raise TemplateException
        else:
            return result


class TemplateException(Exception):
    pass

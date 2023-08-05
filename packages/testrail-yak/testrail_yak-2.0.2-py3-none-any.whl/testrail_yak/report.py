#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class Report(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_reports(self, project_id: int) -> list:
        try:
            result = self.client.send_get(f"get_reports/{project_id}")
        except APIError as error:
            print(error)
            raise ReportException
        else:
            return result

    def run_report(self, report_template_id: int) -> dict:
        try:
            result = self.client.send_get(f"run_report/{report_template_id}")
        except APIError as error:
            print(error)
            raise ReportException
        else:
            return result


class ReportException(Exception):
    pass

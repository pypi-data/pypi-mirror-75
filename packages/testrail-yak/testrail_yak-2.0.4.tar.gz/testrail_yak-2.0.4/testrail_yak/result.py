#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import ResultSchema, TestCaseResultSchema, ResultsSchema, SchemaError


class Result(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_all(self, test_id: int) -> list:
        """Get test results for a given test_id.

        :param test_id:
        :return:
        """
        try:
            result = self.client.send_get(f"get_results/{test_id}")
        except APIError as error:
            print(error)
            raise ResultException
        else:
            return result

    def get_all_from_test_case(self, run_id: int, case_id: int) -> list:
        """Get test results for a given test case.

        :param run_id:
        :param case_id:
        :return:
        """
        try:
            result = self.client.send_get(f"get_results_for_case/{run_id}/{case_id}")
        except APIError as error:
            print(error)
            raise ResultException
        else:
            return result

    def get_all_from_test_run(self, run_id: int) -> list:
        """Get test results for a given test run.

        :param run_id:
        :return:
        """
        try:
            result = self.client.send_get(f"get_results_for_run/{run_id}")
        except APIError as error:
            print(error)
            raise ResultException
        else:
            return result

    def add(self, test_id: int, data: dict) -> dict:
        """Adds a new test result, comment or assigns a test.

        It’s recommended to use add_results instead if you plan to add results for multiple tests.
        """
        try:
            data = ResultSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_result/{test_id}", data=data)
            except APIError as error:
                print(error)
                raise ResultException
            else:
                return result

    def add_to_test_case(self, run_id: int, case_id: int, data: dict) -> dict:
        """Adds a new test result, comment or assigns a test (for a test run and case combination).

        It’s recommended to use add_results_for_cases instead if you plan to add results for multiple test cases.
        """
        try:
            data = TestCaseResultSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_result_for_case/{run_id}/{case_id}", data=data)
            except APIError as error:
                print(error)
                raise ResultException
            else:
                return result

    def add_results(self, run_id: int, data: dict) -> list:
        try:
            data = ResultsSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_results/{run_id}", data=data)
            except APIError as error:
                print(error)
                raise ResultException
            else:
                return result

    def add_results_to_case(self, run_id: int, data: dict) -> list:
        try:
            data = ResultsSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_results_for_cases/{run_id}", data=data)
            except APIError as error:
                print(error)
                raise ResultException
            else:
                return result


class ResultException(Exception):
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class Test:

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_testrun_test(self, test_id: int) -> dict:
        """Get an individual test.

        :param test_id: ID of the individual test
        :return: response from TestRail API containing the test
        """
        try:
            result = self.client.send_get(f"get_test/{test_id}")
        except APIError as error:
            print(error)
            raise TestException
        else:
            return result

    def get_testrun_tests(self, run_id: int) -> list:
        """Get a collection of individual tests by run_id.

        :param run_id: ID of the test run
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_tests/{run_id}")
        except APIError as error:
            print(error)
            raise TestException
        else:
            return result


class TestException(Exception):
    pass

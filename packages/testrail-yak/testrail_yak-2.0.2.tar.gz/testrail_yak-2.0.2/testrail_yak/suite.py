#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import TestSuiteSchema, TestSuiteUpdateSchema, SchemaError


class Suite(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_test_suite(self, suite_id: int) -> dict:
        """Get a test suite by suite_id.

        :param suite_id: ID of the test suite
        :return: response from TestRail API containing the test suites
        """
        try:
            result = self.client.send_get(f"get_suite/{suite_id}")
        except APIError as error:
            print(error)
            raise SuiteException
        else:
            return result

    def get_test_suites(self, project_id: int) -> list:
        """Get a list of test suites associated with a given project_id.

        :param project_id: project ID of the TestRail project
        :return: response from TestRail API containing the test suites
        """
        try:
            result = self.client.send_get(f"get_suites/{project_id}")
        except APIError as error:
            print(error)
            raise SuiteException
        else:
            return result

    def add_test_suite(self, project_id: int, data: dict) -> dict:
        """Add a new test suite to a TestRail project.

        :param project_id: ID of the TestRail project
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test suite
        """
        try:
            data = TestSuiteSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_suite/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise SuiteException
            else:
                return result

    def update_test_suite(self, suite_id: int, data: dict) -> dict:
        """Add a new test suite to a TestRail project.

        :param suite_id: ID of the test suite
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test suite
        """
        try:
            data = TestSuiteUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_suite/{suite_id}", data=data)
            except APIError as error:
                print(error)
                raise SuiteException
            else:
                return result

    def delete_test_suite(self, suite_id: int) -> dict:
        """Add a new test suite to a TestRail project.

        :param suite_id: ID of the test suite
        :return: response from TestRail API containing the newly created test suite
        """
        try:
            result = self.client.send_post(f"delete_suite/{suite_id}", data=None)
        except APIError as error:
            print(error)
            raise SuiteException
        else:
            return result


class SuiteException(Exception):
    pass

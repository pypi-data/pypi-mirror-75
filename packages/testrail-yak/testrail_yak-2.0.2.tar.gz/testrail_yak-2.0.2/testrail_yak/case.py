#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import TestCaseSchema, TestCaseUpdateSchema, SchemaError


class Case(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_test_cases(self, project_id: int) -> list:
        """Get a list of test cases associated with a given project_id.

        :param project_id: project ID of the TestRail project
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_cases/{project_id}")
        except APIError as error:
            print(error)
            raise TestCaseException
        else:
            return result

    def get_test_case(self, case_id: int) -> dict:
        """Get a test case by case_id.

        :param case_id: ID of the test case
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_case/{case_id}")
        except APIError as error:
            print(error)
            raise TestCaseException
        else:
            return result

    def add_test_case(self, section_id: int, data: dict) -> dict:
        """Add a test case to a project by section_id.

        :param section_id: ID of the TestRail section
        :param data:
        :return: response from TestRail API containing the newly created test case
        """
        try:
            data = TestCaseSchema().load(data, partial=True)
        except SchemaError:
            raise TestCaseException
        else:
            try:
                result = self.client.send_post(f"add_case/{section_id}", data=data)
            except APIError as error:
                print(error)
                raise TestCaseException
            else:
                return result

    def update_test_case(self, case_id: int, data: dict) -> dict:
        """Update a test case.

        :param case_id: ID of the TestRail test case
        :param data:
        :return: response from TestRail API containing the newly created test case
        """
        try:
            data = TestCaseUpdateSchema().load(data, partial=True)
        except SchemaError:
            raise TestCaseException
        else:
            try:
                result = self.client.send_post(f"update_case/{case_id}", data=data)
            except APIError as error:
                print(error)
                raise TestCaseException
            else:
                return result

    def delete_test_case(self, case_id: int) -> dict:
        """Delete a test case. """
        try:
            result = self.client.send_post(f"delete_case/{case_id}", data={})
        except APIError as error:
            print(error)
            raise TestCaseException
        else:
            return result


class TestCaseException(Exception):
    pass

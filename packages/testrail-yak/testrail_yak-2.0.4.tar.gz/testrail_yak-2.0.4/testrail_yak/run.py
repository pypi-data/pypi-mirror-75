#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import TestRunSchema, TestRunUpdateSchema, SchemaError


class Run(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get(self, run_id: int) -> dict:
        """Get a test run by run_id.

        :param run_id: ID of the test run
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_run/{run_id}")
        except APIError as error:
            print(error)
            raise RunException
        else:
            return result

    def get_all(self, project_id: int) -> list:
        """Get a list of test runs associated with a given project_id.

        :param project_id: project ID of the TestRail project
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_runs/{project_id}")
        except APIError as error:
            print(error)
            raise RunException
        else:
            return result

    def add(self, project_id: int, data: dict) -> dict:
        """Add a test run to a project.

        Supported fields:

            suite_id (int)
                The ID of the test suite for the test run (optional if the project is operating in single suite mode, required otherwise)

            name (string)
                The name of the test run

            description (string)
                The description of the test run

            milestone_id (int)
                The ID of the milestone to link to the test run

            assignedto_id
                int
                The ID of the user the test run should be assigned to

            include_all	(bool)
                True for including all test cases of the test suite and false for a custom case selection (default: true)

            case_ids (array)
                An array of case IDs for the custom case selection

            refs (string)
                A comma-separated list of references/requirements

        :param project_id: ID of the TestRail project
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test run
        """
        try:
            data = TestRunSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_run/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise RunException
            else:
                return result

    def update(self, run_id: int, data: dict) -> dict:
        """Update a test run in a project.

        Supported fields:

            name (string)
                The name of the test run

            description (string)
                The description of the test run

            milestone_id (int)
                The ID of the milestone to link to the test run

            include_all	(bool)
                True for including all test cases of the test suite and false for a custom case selection (default: true)

            case_ids (array)
                An array of case IDs for the custom case selection

            refs (string)
                A comma-separated list of references/requirements

        :param run_id:
        :param data: request data dictionary
        :return:
        """
        try:
            data = TestRunUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_run/{run_id}", data=data)
            except APIError as error:
                print(error)
                raise RunException
            else:
                return result

    def close(self, run_id: int) -> dict:
        """Close out a test run.

        :param run_id:
        :return:
        """
        try:
            result = self.client.send_post(f"close_run/{run_id}", data=None)
        except APIError as error:
            print(error)
            raise RunException
        else:
            return result

    def delete(self, run_id: int) -> dict:
        """Delete a test run.

        :param run_id:
        :return:
        """
        try:
            result = self.client.send_post(f"delete_run/{run_id}", data=None)
        except APIError as error:
            print(error)
            raise RunException
        else:
            return result


class RunException(Exception):
    pass

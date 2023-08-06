#!/usr/bin/env python
# -*- coding: utf-8 -*-
from testrail_yak.lib.testrail import APIError
from .lib.schema import (
    TestPlanSchema, 
    TestPlanUpdateSchema, 
    TestPlanEntrySchema, 
    TestPlanEntryUpdateSchema, 
    SchemaError
)


class Plan(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get(self, plan_id: int) -> dict:
        """Get a test plan by plan_id.

        :param plan_id: ID of the test plan
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_plan/{plan_id}")
        except APIError as error:
            print(error)
            raise PlanException
        else:
            return result

    def get_all(self, project_id: int) -> list:
        """Get a list of test plans associated with a given project_id.

        :param project_id: project ID of the TestRail project
        :return: response from TestRail API containing the test cases
        """
        try:
            result = self.client.send_get(f"get_plans/{project_id}")
        except APIError as error:
            print(error)
            raise PlanException
        else:
            return result

    def add(self, project_id: int, data: dict) -> dict:
        """Add a test plan to a project.

        :param project_id: ID of the TestRail project
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test plan
        """
        try:
            data = TestPlanSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_plan/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise PlanException
            else:
                return result

    def add_entry(self, plan_id: int, data: dict) -> dict:
        """ Adds one or more new test runs to a test plan. """
        try:
            data = TestPlanEntrySchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_plan_entry/{plan_id}", data=data)
            except APIError as error:
                print(error)
                raise PlanException
            else:
                return result

    def update(self, plan_id: int, data: dict) -> dict:
        """Updates an existing test plan (partial updates are supported, i.e. you can submit and update specific fields only). """
        try:
            data = TestPlanUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_plan/{plan_id}", data=data)
            except APIError as error:
                print(error)
                raise PlanException
            else:
                return result

    def update_entry(self, plan_id: int, entry_id: int, data: dict) -> dict:
        """Updates one or more groups of test runs in a plan (partial updates are supported, i.e. you can submit and update specific fields only). """
        try:
            data = TestPlanEntryUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_plan_entry/{plan_id}/{entry_id}", data=data)
            except APIError as error:
                print(error)
                raise PlanException
            else:
                return result

    def close(self, plan_id: int) -> dict:
        """Closes an existing test plan and archives its test runs & results. """
        try:
            result = self.client.send_post(f"close_plan/{plan_id}", data=None)
        except APIError as error:
            print(error)
            raise PlanException
        else:
            return result

    def delete(self, plan_id: int) -> dict:
        """Deletes an existing test plan. """
        try:
            result = self.client.send_post(f"delete_plan/{plan_id}", data=None)
        except APIError as error:
            print(error)
            raise PlanException
        else:
            return result

    def delete_entry(self, plan_id: int, entry_id: int) -> dict:
        try:
            result = self.client.send_post(f"delete_plan_entry/{plan_id}/{entry_id}", data=None)
        except APIError as error:
            print(error)
            raise PlanException
        else:
            return result


class PlanException(Exception):
    pass

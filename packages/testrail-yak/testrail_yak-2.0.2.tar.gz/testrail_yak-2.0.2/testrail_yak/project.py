#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import ProjectSchema, ProjectUpdateSchema, SchemaError


class Project(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_project(self, project_id: int) -> dict:
        """Get a single project from the TestRail API by passing in its project_id.

        :param project_id: project ID of the TestRail project
        :return: response from TestRail API containing the project
        """
        try:
            result = self.client.send_get(f"get_project/{project_id}")
        except APIError as error:
            print(error)
            raise ProjectException
        else:
            return result

    def get_projects(self) -> list:
        """Get all projects from the TestRail API."""
        try:
            result = self.client.send_get("get_projects")
        except APIError as error:
            print(error)
            raise ProjectException
        else:
            return result

    def add_project(self, data: dict) -> dict:
        """Add a new project to TestRail.

        :param data: request data dictionary
        :return: response from TestRail API containing the newly created project
        """
        try:
            data = ProjectSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post("add_project", data=data)
            except APIError as error:
                print(error)
                raise ProjectException
            else:
                return result

    def update_project(self, project_id: int, data: dict) -> dict:
        """Updates an existing project (admin status required; partial updates are supported, i.e. you can submit and update specific fields only). """
        try:
            data = ProjectUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_project/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise ProjectException
            else:
                return result

    def delete_project(self, project_id: int) -> dict:
        """Deletes an existing project (admin status required). """
        try:
            result = self.client.send_post(f"delete_project/{project_id}", data=None)
        except APIError as error:
            print(error)
            raise ProjectException
        else:
            return result


class ProjectException(Exception):
    pass

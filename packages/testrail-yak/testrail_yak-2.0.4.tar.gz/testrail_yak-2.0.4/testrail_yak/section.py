#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import SectionSchema, SectionUpdateSchema, SchemaError


class Section(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get(self, section_id: int) -> dict:
        """Get test section from a test suite by section_id.

        :param section_id: section ID to grab section from
        :return: response from TestRail API containing the test section
        """
        try:
            result = self.client.send_get(f"get_section/{section_id}")
        except APIError as error:
            print(error)
            raise SectionException
        else:
            return result

    def get_all(self, project_id: int) -> list:
        """Get a list of test sections associated with a project_id and an optional suite_id

        :param project_id:
        :return: response from TestRail API containing the collection of sections
        """
        try:
            result = self.client.send_get(f"get_sections/{project_id}")
        except APIError as error:
            print(error)
            raise SectionException
        else:
            return result

    def get_by_suite_id(self, project_id: int, suite_id: int) -> list:
        """Get a list of test sections associated with a project_id and an optional suite_id

        :param project_id:
        :param suite_id:
        :return: response from TestRail API containing the collection of sections
        """
        try:
            result = self.client.send_get(f"get_sections/{project_id}&suite_id={suite_id}")
        except APIError as error:
            print(error)
            raise SectionException
        else:
            return result

    def add(self, project_id: int, data: dict) -> dict:
        """Add a new section representing a "sprint" to a TestRail project.

        For readability, this separate method is just for adding parent sections (Jira sprints) vs child sections (Jira stories).

        To populate a new child section with a Jira story, use add_story_section() and give it the id value returned here.

        :param project_id: project ID of the TestRail project
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test section
        """
        try:
            data = SectionSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_section/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise SectionException
            else:
                return result

    def add_child(self, project_id: int, parent_id: int, data: dict) -> dict:
        """Add a new child section representing a "story" to a TestRail project. The differentiating factor is the parent ID value.

        This section will be assigned to a parent/child relationship with a parent section, thus parent_id is required.

        Use the id value returned by add_sprint_section as the parent_id.

        Because of this parent id requirement, no suite_id will be needed. If it is ever used in the future, add_sprint_section is the more appropriate place for it.

        :param project_id: project ID of the TestRail project
        :param parent_id: ID of the parent section
        :param data: request data dictionary
        :return: response from TestRail API containing the newly created test section
        """
        data["parent_id"] = parent_id
        try:
            data = SectionSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_section/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise SectionException
            else:
                return result

    def update(self, section_id: int, data: dict) -> dict:
        """Updates an existing section (partial updates are supported, i.e. you can submit and update specific fields only). """
        try:
            data = SectionUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_section/{section_id}", data=data)
            except APIError as error:
                print(error)
                raise SectionException
            else:
                return result

    def delete(self, section_id: int) -> dict:
        """Deletes an existing section. """
        try:
            result = self.client.send_post(f"delete_section/{section_id}", data=None)
        except APIError as error:
            print(error)
            raise SectionException
        else:
            return result


class SectionException(Exception):
    pass

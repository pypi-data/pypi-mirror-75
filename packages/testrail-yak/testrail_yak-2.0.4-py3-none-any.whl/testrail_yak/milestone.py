#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
from .lib.schema import MilestoneSchema, MilestoneUpdateSchema, SchemaError


class Milestone(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get(self, milestone_id: int) -> dict:
        """Returns an existing milestone. """
        try:
            result = self.client.send_get(f"get_milestone/{milestone_id}")
        except APIError as error:
            print(error)
            raise MilestoneException
        else:
            return result

    def get_all(self, project_id: int) -> list:
        """Returns the list of milestones for a project. """
        try:
            result = self.client.send_get(f"get_milestones/{project_id}")
        except APIError as error:
            print(error)
            raise MilestoneException
        else:
            return result

    def add(self, project_id: int, data: dict) -> dict:
        """Creates a new milestone. """
        try:
            data = MilestoneSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"add_milestone/{project_id}", data=data)
            except APIError as error:
                print(error)
                raise MilestoneException
            else:
                return result

    def update(self, milestone_id: int, data: dict) -> dict:
        """Updates an existing milestone (partial updates are supported, i.e. you can submit and update specific fields only). """
        try:
            data = MilestoneUpdateSchema().load(data, partial=True)
        except SchemaError as err:
            raise err
        else:
            try:
                result = self.client.send_post(f"update_milestone/{milestone_id}", data=data)
            except APIError as error:
                print(error)
                raise MilestoneException
            else:
                return result

    def delete(self, milestone_id: int) -> dict:
        """ Deletes an existing milestone. """
        try:
            result = self.client.send_post(f"delete_milestone/{milestone_id}", data=None)
        except APIError as error:
            print(error)
            raise MilestoneException
        else:
            return result


class MilestoneException(Exception):
    pass

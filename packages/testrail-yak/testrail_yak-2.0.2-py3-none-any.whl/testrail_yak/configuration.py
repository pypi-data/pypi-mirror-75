#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class Configuration(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_configs(self, project_id: int) -> list:
        """Returns a list of available configurations, grouped by configuration groups. """
        try:
            result = self.client.send_get(f"get_configs/{project_id}")
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def add_config_group(self, project_id: int, name: str) -> dict:
        """Creates a new configuration group. """
        try:
            result = self.client.send_post(f"add_config_group/{project_id}", data={"name": name})
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def add_config(self, config_group_id: int, name: str) -> dict:
        """Creates a new configuration. """
        try:
            result = self.client.send_post(f"add_config/{config_group_id}", data={"name": name})
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def update_config_group(self, config_group_id: int, name: str) -> dict:
        """Updates an existing configuration group. """
        try:
            result = self.client.send_post(f"update_config_group/{config_group_id}", data={"name": name})
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def update_config(self, config_id: int, name: str) -> dict:
        """Updates an existing configuration. """
        try:
            result = self.client.send_post(f"update_config/{config_id}", data={"name": name})
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def delete_config_group(self, config_group_id: int) -> dict:
        """Deletes an existing configuration group and its configurations. """
        try:
            result = self.client.send_post(f"delete_config_group/{config_group_id}", data=None)
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result

    def delete_config(self, config_id: int) -> dict:
        """Deletes an existing configuration. """
        try:
            result = self.client.send_post(f"delete_config/{config_id}", data=None)
        except APIError as error:
            print(error)
            raise ConfigException
        else:
            return result


class ConfigException(Exception):
    pass

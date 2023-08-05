#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError


class User:

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def get_user(self, user_id: int):
        """Get a TestRail user by user_id.

        :param user_id: user ID of the user we want to grab
        :return: response from TestRail API containing the user
        """
        try:
            result = self.client.send_get(f"get_user/{user_id}")
        except APIError as error:
            print(error)
            raise UserException
        else:
            return result

    def get_user_by_email(self, email_addr: str):
        """Get a TestRail user by email.

        :param email_addr: email address of the user we want to grab
        :return: response from TestRail API containing the user
        """
        try:
            result = self.client.send_get(f"get_user_by_email&email={email_addr}")
        except APIError as error:
            print(error)
            raise UserException
        else:
            return result

    def get_users(self):
        """Get a list of TestRail users.

        :return: response from TestRail API containing the user collection
        """
        try:
            result = self.client.send_get("get_users")
        except APIError as error:
            print(error)
            raise UserException
        else:
            return result


class UserException(Exception):
    pass

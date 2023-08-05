#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .lib.testrail import APIError
import os


class Attachment(object):

    __module__ = "testrail_yak"

    def __init__(self, api):
        self.client = api

    def attach_to_plan(self, plan_id: int, file_path: str) -> dict:
        """Adds an attachment to a test plan. The maximum allowable upload size is set to 256mb. """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise AttachmentException

        try:
            result = self.client.send_post(f"add_attachment_to_plan/{plan_id}", data=file_path)
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def attach_to_plan_entry(self, plan_id: int, entry_id: int, file_path: str) -> dict:
        """Adds an attachment to a test plan entry. The maximum allowable upload size is set to 256mb. """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise AttachmentException

        try:
            result = self.client.send_post(f"add_attachment_to_plan_entry/{plan_id}/{entry_id}", data=file_path)
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def attach_to_result(self, result_id: int, file_path: str) -> dict:
        """Adds attachment to a result based on the result ID. The maximum allowable upload size is set to 256mb. """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise AttachmentException

        try:
            result = self.client.send_post(f"add_attachment_to_result/{result_id}", data=file_path)
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def attach_to_run(self, run_id: int, file_path: str) -> dict:
        """Adds attachment to test run. The maximum allowable upload size is set to 256mb. """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise AttachmentException

        try:
            result = self.client.send_post(f"add_attachment_to_run/{run_id}", data=file_path)
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_case_attachments(self, case_id: int) -> list:
        """Returns a list of attachments for a test case. """
        try:
            result = self.client.send_get(f"get_attachments_for_case/{case_id}")
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_plan_attachments(self, plan_id: int) -> list:
        """Returns a list of attachments for a test plan. """
        try:
            result = self.client.send_get(f"get_attachments_for_plan/{plan_id}")
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_plan_entry_attachments(self, plan_id: int, entry_id: int) -> list:
        """Returns a list of attachments for a test plan entry. """
        try:
            result = self.client.send_get(f"get_attachments_for_plan_entry/{plan_id}/{entry_id}")
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_run_attachments(self, run_id: int) -> list:
        """Returns a list of attachments for a test run. """
        try:
            result = self.client.send_get(f"get_attachments_for_run/{run_id}")
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_test_attachments(self, test_id: int) -> list:
        """Returns a list of attachments for a test’s results. """
        try:
            result = self.client.send_get(f"get_attachments_for_test/{test_id}")
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def get_attachment(self, attachment_id: int, filepath: str) -> dict:
        """Retrieves the requested file identified by :attachment_id. """
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise AttachmentException

        try:
            result = self.client.send_get(f"get_attachment/{attachment_id}", filepath=filepath)
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result

    def delete_attachment(self, attachment_id: int) -> dict:
        """Deletes the specified attachment identified by :attachment_id. """
        try:
            result = self.client.send_post(f"delete_attachment/{attachment_id}", data={})
        except APIError as error:
            print(error)
            raise AttachmentException
        else:
            return result


class AttachmentException(Exception):
    pass

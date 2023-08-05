#!/usr/bin/env python
# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, ValidationError


class SchemaError(ValidationError):
    pass


class TestCaseSchema(Schema):
    title               = fields.Str(required=True)
    template_id         = fields.Int()
    type_id             = fields.Int()
    priority_id         = fields.Int()
    estimate            = fields.Str()
    milestone_id        = fields.Int()
    refs                = fields.Str()


class TestCaseUpdateSchema(Schema):
    title               = fields.Str()
    template_id         = fields.Int()
    type_id             = fields.Int()
    priority_id         = fields.Int()
    estimate            = fields.Str()
    milestone_id        = fields.Int()
    refs                = fields.Str()

class CaseFieldSchema(Schema):
    type                = fields.Str(required=True)
    name                = fields.Str(required=True)
    label               = fields.Str(required=True)
    description         = fields.Str()
    include_all         = fields.Bool()
    template_ids        = fields.List(fields.Int())
    configs             = fields.List(fields.Dict(), required=True)


class MilestoneSchema(Schema):
    name                = fields.Str(required=True)
    description         = fields.Str()
    due_on              = fields.Int()
    parent_id           = fields.Int()
    start_on            = fields.Int()


class MilestoneUpdateSchema(Schema):
    name                = fields.Str()
    description         = fields.Str()
    due_on              = fields.Int()
    parent_id           = fields.Int()
    start_on            = fields.Int()
    is_completed        = fields.Bool()
    is_started          = fields.Bool()


class TestPlanSchema(Schema):
    name                = fields.Str(required=True)
    description         = fields.Str()
    milestone_id        = fields.Int()
    entries             = fields.List(fields.Dict())


class TestPlanUpdateSchema(Schema):
    name                = fields.Str()
    description         = fields.Str()
    milestone_id        = fields.Int()


class TestPlanEntrySchema(Schema):
    suite_id            = fields.Int(required=True)
    name                = fields.Str()
    description         = fields.Str()
    assignedto_id       = fields.Int()
    include_all         = fields.Bool()
    case_ids            = fields.List(fields.Int())
    config_ids          = fields.List(fields.Int())
    refs                = fields.Str()
    runs                = fields.List(fields.Dict())


class TestPlanEntryUpdateSchema(Schema):
    name                = fields.Str()
    description         = fields.Str()
    assignedto_id       = fields.Int()
    include_all         = fields.Bool()
    case_ids            = fields.List(fields.Int())
    refs                = fields.Str()


class ProjectSchema(Schema):
    name                = fields.Str(required=True)
    announcement        = fields.Str()
    show_announcement   = fields.Bool()
    suite_mode          = fields.Int()


class ProjectUpdateSchema(Schema):
    name                = fields.Str()
    announcement        = fields.Str()
    show_announcement   = fields.Bool()
    is_completed        = fields.Bool()


class ResultSchema(Schema):
    status_id           = fields.Int(required=True)
    comment             = fields.Str()
    version             = fields.Str()
    elapsed             = fields.Str()
    defects             = fields.Str()
    assignedto_id       = fields.Int()


class ResultsSchema(Schema):
    results             = fields.List(fields.Dict())


class TestCaseResultSchema(Schema):
    status_id           = fields.Int(required=True)
    comment             = fields.Str()
    version             = fields.Str()
    elapsed             = fields.Str()
    defects             = fields.Str()
    assignedto_id       = fields.Int()


class TestRunSchema(Schema):
    suite_id            = fields.Int()
    name                = fields.Str()
    description         = fields.Str()
    milestone_id        = fields.Int()
    assignedto_id       = fields.Int()
    include_all         = fields.Bool()
    case_ids            = fields.List(fields.Int())
    refs                = fields.Str()


class TestRunUpdateSchema(Schema):
    name                = fields.Str()
    description         = fields.Str()
    milestone_id        = fields.Int()
    include_all         = fields.Bool()
    case_ids            = fields.List(fields.Int())
    refs                = fields.Str()


class SectionSchema(Schema):
    description         = fields.Str()
    suite_id            = fields.Int()
    parent_id           = fields.Int()
    name                = fields.Str(required=True)


class SectionUpdateSchema(Schema):
    description         = fields.Str()
    name                = fields.Str()


class TestSuiteSchema(Schema):
    name                = fields.Str(required=True)
    description         = fields.Str()


class TestSuiteUpdateSchema(Schema):
    name                = fields.Str()
    description         = fields.Str()

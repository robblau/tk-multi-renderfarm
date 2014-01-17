# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


import tank

class PublishOutput(object):
    """
    Encapsulate an output definition as
    loaded from the configuration
    """

    PRIMARY_NAME = "primary"

    def __init__(self, app, fields={}, name=None, selected=None, required=None):
        """
        Construction
        """
        self._raw_fields = fields

        # special case handling of some fields that can be provided either
        # as args or through the fields
        self._name = (fields.get("name", "") if name is None else name)
        self._required = (fields.get("required", False) if required is None else required)
        self._selected = self._required or (fields.get("selected", True) if selected is None else selected)

        self._template_work = app.get_template_by_name(self._raw_fields['template_work'])
        self._template_job = app.get_template_by_name(self._raw_fields['template_job'])
        self._template_submit = app.get_template_by_name(self._raw_fields['template_submit'])
        self._template_temp = app.get_template_by_name(self._raw_fields['template_temp'])
        self._template_render = app.get_template_by_name(self._raw_fields['template_render'])

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._raw_fields["display_name"]

    @property
    def display_group(self):
        return self._raw_fields.get("display_group", "")

    @property
    def description(self):
        return self._raw_fields["description"]

    @property
    def icon_path(self):
        return self._raw_fields["icon"]

    @property
    def tank_type(self):
        return self._raw_fields["tank_type"]

    @property
    def selected(self):
        return self._selected

    @property
    def required(self):
        return self._required

    @property
    def template_work(self):
        return self._template_work

    @property
    def template_job(self):
        return self._template_job

    @property
    def template_submit(self):
        return self._template_submit

    @property
    def template_temp(self):
        return self._template_temp

    @property
    def template_render(self):
        return self._template_render

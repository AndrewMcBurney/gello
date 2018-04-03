# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""subscribed_lists/forms.py

SubscribedList-related forms.
"""

import textwrap

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from ...models import List, TrelloMember


class NewForm(Form):
    """Form for creating a subscribed_list."""
    list_name = StringField(
        'List Name',
        validators=[Required()],
        description=textwrap.dedent(
            """
            The name of a Trello list associated with the Trello board
            subscribed
            """
        )
    )
    trello_username = StringField(
        'Trello Member Username',
        description=textwrap.dedent(
            """
            An optional field to specify the Trello username for a member to be
            automatically assigned to any Trello cards created on this list
            """
        )
    )
    submit = SubmitField('Create')

    def __init__(self, board_id):
        """Sets the `board_id` for the form."""
        Form.__init__(self)
        self._board_id = board_id

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `list_id` attribute is a `List.trello_list_id`
          belonging to the `Board` with `board_id`.
        - Validates the `trello_member_id `attribute belongs to a
          `TrelloMember`
        """
        list_name = self.list_name.data.strip()
        trello_username = self.trello_username.data.strip()

        trello_list = List.query.filter_by(
            name=list_name, board_id=self._board_id
        ).first()

        if trello_list is None:
            return False
        self._list_id = trello_list.trello_list_id

        # `trello_member_id` is optional
        if not trello_username:
            return True

        trello_member = TrelloMember.query.filter_by(
            username=trello_username
        ).first()

        if trello_member is None:
            return False

        self._trello_member_id = trello_member.trello_member_id
        return True

    def get_list_id(self):
        return self._list_id

    def get_trello_member_id(self):
        return self._trello_member_id


class DeleteForm(Form):
    """Form for deleting an existing subscribed_list."""
    submit = SubmitField('Delete')

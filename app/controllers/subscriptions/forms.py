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

"""subscriptions/forms.py

Subscription-related forms.
"""

import re
import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from ...models import Board, Repo, Subscription


class NewSubscriptionForm(FlaskForm):
    """Form for creating a new subscription."""
    board_name = StringField(
        'Board Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name of a Trello board you wish to subscribe
            """
        )
    )
    repo_name = StringField(
        'Repo Name',
        validators=[Required(), Length(1, 100)],
        description=textwrap.dedent(
            """
            The name of a GitHub repository you wish to register event webhooks
            for
            """
        )
    )
    issue_autocard = BooleanField(
        'Issue Autocard',
        description=textwrap.dedent(
            """
            If checked, trello cards will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-issues/'>GitHub
            Issue</a>.
            """
        )
    )
    pull_request_autocard = BooleanField(
        'Pull Request Autocard',
        description=textwrap.dedent(
            """
            If checked, trello cards will automatically be created when a
            contributor outside of your organization submits a
            <a href='https://help.github.com/articles/about-pull-requests/'>
            Pull Request</a>.
            """
        )
    )
    submit = SubmitField('Create')

    def validate(self):
        """Performs validations of the form field values.

        - Validates the `board_id `attribute belongs to a `Board`
        - Validates the `repo_id `attribute belongs to a `Repo`
        """
        board_name = self.board_name.data.strip()
        repo_name = self.repo_name.data.strip()

        # Perform board-specific validations
        board = Board.query.filter_by(name=board_name).first()
        if board is None:
            self._error_message = textwrap.dedent(
                f"""
                Board '{board_name}' does not exist
                """
            )
            return False

        # Get the `board_id` to return back to `views.py`
        self._board_id = board.trello_board_id

        # Perform repo-specific validations
        repo = Repo.query.filter_by(name=repo_name).first()
        if repo is None:
            self._error_message = textwrap.dedent(
                f"""
                Repo '{repo_name}' does not exist
                """
            )
            return False

        # Get the `repo_id` to return back to `views.py`
        self._repo_id = repo.github_repo_id

        # Validate the `Subscription` does not already exist
        subscription = Subscription.query.get([self._board_id, self._repo_id])
        if subscription is not None:
            self._error_message = textwrap.dedent(
                f"""
                Subscription exists for {board_name} and {repo_name}
                """
            )
            return False

        # All custom validations passed
        return True

    def get_board_id(self):
        return self._board_id

    def get_repo_id(self):
        return self._repo_id

    def get_error_message(self):
        return self._error_message


class UpdateForm(FlaskForm):
    """Form for updating an existing subscription."""
    issue_autocard = BooleanField('Issue Autocard')
    pull_request_autocard = BooleanField('Pull Request Autocard')
    submit = SubmitField('Update')


class DeleteForm(FlaskForm):
    """Form for deleting an existing subscription."""
    submit = SubmitField('Delete')

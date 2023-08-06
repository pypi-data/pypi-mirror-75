# Copyright (C) 2020  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Unit tests for the message schema."""

import pytest

from jsonschema import ValidationError
from ..messages import RepoUpdateV1
from .utils import DUMMY_UPDATE


def test_repo_update_v1():
    """
    Assert the message schema validates a message with the required fields.
    """
    body = DUMMY_UPDATE
    message = RepoUpdateV1(body=body)
    message.validate()


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {}
    message = RepoUpdateV1(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_str():
    """Assert __str__ produces a human-readable message."""
    body = DUMMY_UPDATE
    expected_str = (
        "MDAPI updated repo rawhide with new details for the packages: kernel, inkscape"
    )
    message = RepoUpdateV1(body=body)
    message.validate()
    assert expected_str == str(message)


def test_summary():
    """Assert the summary is correct."""
    body = DUMMY_UPDATE
    expected_summary = "MDAPI updated repo rawhide with new details for 2 packages"
    message = RepoUpdateV1(body=body)
    assert expected_summary == message.summary

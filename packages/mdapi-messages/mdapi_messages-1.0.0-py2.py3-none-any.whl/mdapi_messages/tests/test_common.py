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

"""Unit tests for common properties of the message schemas."""

from ..messages import RepoUpdateV1
from .utils import DUMMY_UPDATE


def test_properties():
    """Assert some properties are correct."""
    body = DUMMY_UPDATE
    message = RepoUpdateV1(body=body)

    assert message.app_name == "mdapi"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/mdapi.png"

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

from .base import SCHEMA_URL, mdapiMessage


class RepoUpdateV1(mdapiMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by mdapi when a repo's info is updated.
    """

    topic = "mdapi.repo.update"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a repo is updated",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "packages": {"type": "array", "contains": {"type": "string"}},
            "url": {"type": "string", "format": "uri"},
        },
        "required": ["name", "packages"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return (
            f"MDAPI updated repo {self.body['name']} with new details for the packages: "
            f"{', '.join(p for p in self.body['packages'])}"
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        return (
            f"MDAPI updated repo {self.body['name']} with new details for "
            f"{len(self.body['packages'])} packages"
        )

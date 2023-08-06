# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) Treble.ai
#
# Licensed under the terms of the MIT License
# (see LICENSE.txt for details)
# -----------------------------------------------------------------------------

"""Simple Python ORM for PostgresDB."""

from .dbsession import DBConnection, DatabaseObject, DBSession

DBSession
DBConnection
DatabaseObject

VERSION_INFO = (0, 6, 0)
__version__ = '.'.join(map(str, VERSION_INFO))

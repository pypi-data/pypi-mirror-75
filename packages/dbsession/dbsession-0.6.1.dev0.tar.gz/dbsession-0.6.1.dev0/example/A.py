# -*- coding: utf-8 -*-

from dbsession import DatabaseObject

TABLE_NAME = 'A'


class _A(DatabaseObject):

    _TABLE_NAME = TABLE_NAME

    def __init__(self, row):
        super().__init__(row)


wrapper = _A


def find_by_id(a_id):
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE id = %s
    """

    values = (a_id, )

    return query, values, wrapper, False


def get_all():
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
    """

    values = ()

    return query, values, wrapper, True

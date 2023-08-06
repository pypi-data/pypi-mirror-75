from dbsession import DatabaseObject

import sys
current_module = sys.modules[__name__]

TABLE_NAME = 'company'

class _A(DatabaseObject):

    _TABLE_NAME = TABLE_NAME

    def __init__(self, row):
        super().__init__(row)


wrapper = _A

from .B import set_default_querys

set_default_querys(current_module,TABLE_NAME,wrapper)


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

    values = ( )

    return query, values, wrapper, True


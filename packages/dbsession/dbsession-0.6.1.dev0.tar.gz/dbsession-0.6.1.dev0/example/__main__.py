# -*- coding: utf-8 -*-

from .A import find_by_id, get_all
from .config import db_connection


if __name__ == "__main__":
    db_session = db_connection.get_session()
    a_1 = db_session.query(find_by_id, 1)
    print(a_1)

    all_a = db_session.query(get_all)
    print(all_a)

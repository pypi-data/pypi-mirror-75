import sys
current_module = sys.modules[__name__]


def set_default_querys(module, TABLE_NAME, wrapper):
	setattr(module, 'find_by_ids', f(TABLE_NAME, wrapper))



def f(TABLE_NAME, wrapper):
	def find_by_ids(a_id):
    
	    query = f"""
	        SELECT *
	        FROM {TABLE_NAME}
	        WHERE id = %s
	    """

	    values = (a_id, )

	    return query, values, wrapper, False

	return find_by_ids
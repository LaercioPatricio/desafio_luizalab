from math import ceil

MAX_UNLIMITED_PAGE = 100
def Pagination (page, limit, total_count):
	if not isinstance( page, int ) or not isinstance( limit, int ) or not isinstance( total_count, int ):
		raise TypeError

	if total_count == 0 or limit == 0 or page < 0 :
		raise NameError('InvalidPagination')

	pages = int(ceil(total_count / float(min(limit, MAX_UNLIMITED_PAGE))))

	if page > pages :
		raise NameError('InvalidPageRange')

	index_from = page * limit 
	index_to = min(index_from + limit, total_count)

	return {'pages': pages,
			'page': page,
			'total_count': total_count,
			'limit': limit,
			'has_next': page < pages,
			'has_preview': page > 1}
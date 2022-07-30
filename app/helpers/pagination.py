import math


def pagination(page: int, per_page: int, data_list: list, serializer=None) -> dict:
    """
    Genera los links de paginación.
    """
    total_items = data_list.count() if serializer else len(data_list)
    total_pages = math.ceil(total_items / per_page)
    if page > total_pages:
        page = total_pages
    if page < 1:
        page = 1
    start = (page - 1) * per_page
    end = page * per_page

    if serializer:
        data_list = serializer(
            instance=data_list[start:end],
            many=True,
        ).data
    else:
        data_list = data_list[start:end]

    return {
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'prev_page': page - 1 if page > 1 else None,
            'next_page': page + 1 if page < total_pages else None,
            'last_page': total_pages,
        },
        'list': data_list or [],
    }

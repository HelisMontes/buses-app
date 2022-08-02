from rest_framework.parsers import JSONParser


def request(function):
    '''
    Decorador para parsear el payload de la petición
    '''
    def wrapper(*args, **kwargs) -> dict:
        path_params = kwargs
        body = JSONParser().parse(args[0]) if args[0].method == 'POST' else {}
        query_params = {}
        if args[0].method == 'GET':
            for key, value in args[0].query_params.items():
                query_params[key] = value
        page = None
        per_page = None
        if query_params.get('page'):
            page = query_params.get('page')
            if page.isdigit():
                query_params['page'] = int(page)
            else:
                del query_params['page']
        if query_params.get('page') == '':
            del query_params['page']
        if query_params.get('per_page'):
            per_page = query_params.get('per_page')
            if per_page.isdigit():
                query_params['per_page'] = int(per_page)
            else:
                del query_params['per_page']
        if query_params.get('per_page') == '':
            del query_params['per_page']
        if page and per_page:
            if page == 'all' and per_page == 'all':
                query_params['page'] = 'all'
                query_params['per_page'] = 'all'

        if query_params.get('filter_by'):
            filter_by = query_params.get('filter_by')
            filter_value = query_params.get('filter_value')
            if filter_by and filter_value:
                query_params['filter_by'] = filter_by
                query_params['filter_value'] = filter_value
            else:
                del query_params['filter_by']
                if filter_value:
                    del query_params['filter_value']
        if query_params.get('sort_by'):
            sort_by = query_params.get('sort_by')
            sort_type = query_params.get('sort_type')
            if sort_by and sort_type:
                query_params['sort_by'] = sort_by
                query_params['sort_type'] = sort_type
            else:
                del query_params['sort_by']
                if sort_type:
                    del query_params['sort_type']
        return function({
            'body': body or {},
            'query_params': query_params or {},
            'path_params': path_params or {},
        })
    return wrapper

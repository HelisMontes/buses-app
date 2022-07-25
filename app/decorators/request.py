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
        if query_params.get('page'):
            page = query_params.get('page')
            if page.isdigit():
                query_params['page'] = int(page)
            else:
                del query_params['page']
        if query_params.get('per_page'):
            per_page = query_params.get('per_page')
            if per_page.isdigit():
                query_params['per_page'] = int(per_page)
            else:
                del query_params['per_page']
        return function({
            'body': body or {},
            'query_params': query_params or {},
            'path_params': path_params or {},
        })
    return wrapper

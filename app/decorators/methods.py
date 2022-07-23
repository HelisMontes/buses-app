from rest_framework.parsers import JSONParser


def clean_get(function):
    def wrapper(*args, **kwargs) -> dict:
        query_params = args[0].query_params
        query_news = {
            **query_params,
        }
        if query_params.get('page'):
            page = query_params.get('page')
            if page.isdigit():
                page = int(page)
            else:
                page = 1
            query_news['page'] = page
        if query_params.get('per_page'):
            per_page = query_params.get('per_page')
            if per_page.isdigit():
                per_page = int(per_page)
            else:
                per_page = 10
            query_news['per_page'] = per_page
        return function(query_news)
    return wrapper


def clean_post(function):
    def wrapper(*args, **kwargs) -> dict:
        return function(JSONParser().parse(args[0]))
    return wrapper

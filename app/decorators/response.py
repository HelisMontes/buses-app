from django.http import JsonResponse


def response(f):
    '''
    Decorador para la respuesta de la API
    '''
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        data = response.get('data', {})
        message = response.get('message', '')
        status_code = response.get('status_code', 200)

        return JsonResponse(
            {
                'data': data,
                'message': message,
            },
            status=status_code,
            safe=False,
        )
    return wrapped

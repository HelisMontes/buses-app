from django.http import JsonResponse


def response(f):
    '''
    Decorador para la respuesta de la API
    '''
    def wrapped(*args, **kwargs):
        data = {}
        message = None
        status_code = 200
        try:
            response = f(*args, **kwargs)
            data = response.get('data', {})
            message = response.get('message', '')
            status_code = response.get('status_code', 200)
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 500

        response = JsonResponse(
            {
                'data': data,
                'message': message,
            },
            status=status_code,
            safe=False,
        )
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Max-Age'] = '1000'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'

        return response
    return wrapped

from django.http import JsonResponse


def response(f):
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        data = response.get('data', {})
        message = response.get('message', '')
        status = response.get('status', 200)

        return JsonResponse(
            {
                'data': data,
                'message': message,
            },
            status=status,
            safe=False,
        )
    return wrapped

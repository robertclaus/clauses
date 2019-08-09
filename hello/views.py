from django.http import JsonResponse


def index(request):
    data = {
        'message': 'Welcome!',
        'todo': 'Make Landing Page',
    }
    return JsonResponse(data)

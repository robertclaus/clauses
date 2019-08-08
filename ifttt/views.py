from django.core.serializers import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def is_valid(request):
    key = settings.IFTTT_CHANNEL_KEY
    print(f"Headers: {request.META}")
    channel_key = request.META.get("HTTP_IFTTT_CHANNEL_KEY")
    service_key = request.META.get("HTTP_IFTTT_SERVICE_KEY")

    if not channel_key or not service_key or key != channel_key or key != service_key:
        return False


def invalid_response():
    return JsonResponse({"errors": [{"message": "IFTTT sent an OAuth2 access token that isn’t valid."}]}, status=401)


@csrf_exempt
def status(request):
    if not is_valid(request):
        return invalid_response()
    return JsonResponse({"status": "Live"})


@csrf_exempt
def update(request):
    if not is_valid(request):
        return invalid_response()

    print(f"Request GET: {request.GET}")
    print(f"Request POST: {request.POST}")
    print(f"Request Body: {request.body}")

    contents = json.loads(request.body.decode('utf-8'))
    action_fields = contents.get('actionFields')

    if not contents or not action_fields or not action_fields.get('key') or not action_fields.get('code'):
        return JsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    response_contents = {"ok": "True"}
    return JsonResponse(response_contents)


@csrf_exempt
def state(request):
    if not is_valid(request):
        return invalid_response()

    print(f"Request GET: {request.GET}")
    print(f"Request POST: {request.POST}")
    print(f"Request Body: {request.body}")

    contents = json.loads(request.body.decode('utf-8'))
    trigger_fields = contents.get('triggerFields')

    if not contents or not trigger_fields or not trigger_fields.get('key') or not trigger_fields.get('code'):
        return JsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    response_contents = {"ok": "True"}
    return JsonResponse(response_contents)


@csrf_exempt
def test_setup(request):
    if not is_valid(request):
        return invalid_response()

    test_setup_json = {
      "data": {
        "samples": {
          "triggers": {
            "state": {
              "key": "test_123",
              "code": "state.test = True"
            }
          },
          "actions": {
            "update": {
              "key": "test_123",
              "code": "return state.test"
            }
          },
          "actionRecordSkipping": {
            "update": {
              "key": "test_123",
              "code": "return True"
            }
          }
        }
      }
    }

    return JsonResponse(test_setup_json)

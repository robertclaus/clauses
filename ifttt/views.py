from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def is_valid(request):
    key = settings.IFTTT_CHANNEL_KEY
    channel_key = request.get("IFTTT-Channel-Key")
    service_key = request.get("IFTTT-Service-Key")

    if key != channel_key or key != service_key:
        return False


def invalid_response():
    return JsonResponse({"errors": [{"message": "IFTTT sent an OAuth2 access token that isn’t valid."}]}, status=401)


@csrf_exempt
def status(request):
    if not is_valid(request):
        return invalid_response()
    return JsonResponse({"status": "Live"})


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

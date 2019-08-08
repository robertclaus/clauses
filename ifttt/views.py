import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from ifttt.models import Clause


class UTFJsonResponse(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, content_type="application/json; charset=utf-8", **kwargs)


def is_valid(request):
    key = settings.IFTTT_CHANNEL_KEY
    print(f"Headers: {request.META}")
    channel_key = request.META.get("HTTP_IFTTT_CHANNEL_KEY")
    service_key = request.META.get("HTTP_IFTTT_SERVICE_KEY")

    print(f"key={key}, c_key={channel_key}, s_key={service_key}")

    if not channel_key or not service_key or key != channel_key or key != service_key:
        return False

    return True


def invalid_response():
    return UTFJsonResponse({"errors": [{"message": "IFTTT sent an OAuth2 access token that isn’t valid."}]}, status=401)


@csrf_exempt
def status(request):
    if not is_valid(request):
        return invalid_response()
    return UTFJsonResponse({"status": "Live"})


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
        return UTFJsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    key = action_fields.get("code")
    code = action_fields.get("code")

    # TODO take user into account
    clause, created = Clause.objects.get_or_create(key=key, user=None, defaults={"state": "{}"})
    state = json.loads(clause.state)
    exec(code, {}, {"state": state})
    clause.state = state
    clause.save()

    response_contents = {"ok": "True"}
    return UTFJsonResponse(response_contents)


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
        return UTFJsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    key = trigger_fields.get("code")
    code = trigger_fields.get("code")

    # TODO take user into account
    clause = Clause.objects.get_or_create(key=key, user=None, defaults={"state": "{}"})
    state = json.loads(clause.state)

    def code_exec(code, state):
        exec(code, {}, {"state": state})
        return False

    should_trigger = code_exec(code, state)
    clause.state = state
    clause.save()

    response_contents = {"ok": should_trigger}
    return UTFJsonResponse(response_contents)


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

    return UTFJsonResponse(test_setup_json)

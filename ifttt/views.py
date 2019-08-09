from datetime import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from ifttt.models import Clause, Event


class UTFJsonResponse(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=False, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, content_type="application/json; charset=utf-8", **kwargs)


def is_valid(request):
    key = settings.IFTTT_CHANNEL_KEY
    channel_key = request.META.get("HTTP_IFTTT_CHANNEL_KEY")
    service_key = request.META.get("HTTP_IFTTT_SERVICE_KEY")

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

    decoded = request.body.decode('utf-8')
    contents = json.loads(decoded)
    print(f"decoded: {decoded}, json: {contents}")
    action_fields = contents.get('actionFields')

    if not contents or not action_fields or not action_fields.get('key') or not action_fields.get('code'):
        return UTFJsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    key = action_fields.get("key")
    code = action_fields.get("code")

    # TODO take user into account
    clause, created = Clause.objects.get_or_create(key=key, user="test", defaults={"state": '{"test":true}'})
    state = json.loads(clause.state)

    try:
        exec(code)
    except Exception:
        return UTFJsonResponse({"errors": [{"status": "SKIP", "message": "Missing record referred to."}]}, status=400)

    clause.state = json.dumps(state)
    clause.save()
    clause.refresh_from_db()

    notify(clause)

    response_contents = {"data": [{"id": "1"}]}
    return UTFJsonResponse(response_contents)


def notify(clause):
    pass


@csrf_exempt
def state(request):
    if not is_valid(request):
        return invalid_response()

    print(f"Request GET: {request.GET}")
    print(f"Request POST: {request.POST}")
    print(f"Request Body: {request.body}")

    decoded = request.body.decode('utf-8')
    contents = json.loads(decoded)
    print(f"decoded: {decoded}, json: {contents}")
    trigger_fields = contents.get('triggerFields')

    if not contents or not trigger_fields or not trigger_fields.get('key') or not trigger_fields.get('code'):
        return UTFJsonResponse({"errors": [{"message": "Missing Field."}]}, status=400)

    key = trigger_fields.get("key")
    code = trigger_fields.get("code")
    limit = contents.get("limit", 100)

    # TODO take user into account
    clause, created = Clause.objects.get_or_create(key=key, user="test", defaults={"state": '{"test":true}'})
    state = json.loads(clause.state)

    should_trigger = False
    try:
        exec(code)
    except Exception:
        return UTFJsonResponse({"errors": [{"status": "SKIP", "message": "Missing record referred to."}]}, status=400)

    print(f"Should Trigger? : {should_trigger}")

    if should_trigger:
        Event.objects.create(timestamp=datetime.now(), clause=clause)

    clause.state = json.dumps(state)
    clause.save()

    events = Event.objects.filter(clause=clause).order_by('-timestamp')[:limit]

    response_contents = []
    for event in events:
        response_contents.append({
            "meta": {"key": str(event.pk), "id": str(event.pk), "timestamp": str(int(event.timestamp.timestamp()))},
            "created_at": event.timestamp.isoformat(),
        })

    response_contents = {"data": response_contents}

    print(f"response content: {response_contents}")
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
              "code": "should_trigger = True"
            }
          },
          "actions": {
            "update": {
              "key": "test_123",
              "code": "state['test'] = True"
            }
          },
          "actionRecordSkipping": {
            "update": {
              "key": "test_123",
              "code": "test = state.notanattribute"
            }
          }
        }
      }
    }

    return UTFJsonResponse(test_setup_json)

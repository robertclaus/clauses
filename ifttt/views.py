from django.http import JsonResponse


def test_setup(request):
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

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def snapshot_webhook_handler(request):
    # webhook -> POST request
    # django <> POST request without csrf tokens
    if request.method != "POST":
        return HttpResponse("OK")
    
    
    auth = request.headers.get("Authorization")
    if auth.startswith("Basic "):
        token = auth.split(" ")[1]
        if token == "abc1234":
            data = {}
            try:
                data = json.loads(request.body.decode('utf-8'))
            except:
                pass
            print(data)

    return HttpResponse("OK")
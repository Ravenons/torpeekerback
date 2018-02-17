from backend.models import Visit
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from backend.serializers import VisitSerializer
from backend.tasks import visit_url
import uuid

@api_view(['GET', 'PUT'])
def visit_result(request, ref):

    try:
        validated_ref = uuid.UUID(hex=ref)
    except Exception:
        return JsonResponse({}, status=406)

    # We should get a result or no result, otherwise, UUIDv4 colision...
    visits = Visit.objects.filter(ref=validated_ref)
    visits_count =visits.count() 

    if visits_count == 0:
        return JsonResponse({}, status=404)
    elif visits_count == 1:
        visit = visits[0]
        if request.method == 'GET':
            return JsonResponse({'url': visit.url,
                                 'is_ready': visit.is_ready,
                                 'screenshot': visit.screenshot},
                                status=200)
        else: # PUT method
            # Currently just updating is_ready and screenshot...
            validated_request = JSONParser().parse(request)
    
            validated_screenshot = validated_request['screenshot']
            if not validated_screenshot:
                return JsonResponse({}, status=406)

            visit.is_ready = True
            visit.screenshot = validated_screenshot
            visit.save()
            return JsonResponse({}, status=200)
    else:
        # More than 1 result, collision...
        pass

@api_view(['POST'])
def visit(request):

    try:
        validated_request = JSONParser().parse(request)
        validated_url = validated_request['url']
        visit = Visit(url=validated_url)
        visit.save()
    except Exception:
        return JsonResponse({}, status=406)

    ref = visit.ref.hex
    visit_url.delay(validated_url, ref)

    return JsonResponse({'ref': ref},
                        status=200)
     

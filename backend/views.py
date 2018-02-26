from backend.models import Visit
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.serializers import VisitSerializer
from backend.tasks import visit_url
import uuid

@api_view(['GET', 'PUT'])
def visit_result(request, ref):

    try:
        validated_ref = uuid.UUID(hex=ref)
    except Exception:
        return Response({ "error": "Invalid ID format"},
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    # We should get a result or no result, otherwise, UUIDv4 colision...
    visits = Visit.objects.filter(ref=validated_ref)
    visits_count =visits.count() 

    if visits_count == 0:
        return Response({ "error": "ID not found" },
                        status=status.HTTP_404_NOT_FOUND)
    elif visits_count == 1:
        visit = visits[0]
        if request.method == 'GET':
            return Response({'url': visit.url,
                             'is_ready': visit.is_ready,
                             'screenshot': visit.screenshot})
        else: # PUT method
            # Currently just updating is_ready and screenshot...
            screenshot = request.data['screenshot']
            if not screenshot:
                return Response({ "error": "Screenshot not specified" },
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            visit.is_ready = True
            visit.screenshot = screenshot
            visit.save()
            return Response({ "info": "Screenshot successfully stored" })
    else:
        # More than 1 result, collision...
        pass

@api_view(['POST'])
def visit(request):

    try:
        url = request.data['url']
        visit = Visit(url=url)
        visit.save()
    except Exception:
        return Response({ "error": "URL not specified or incorrect format" },
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    ref = visit.ref.hex
    visit_url.delay(url, ref)

    return Response({'ref': ref})

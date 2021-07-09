from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from api.schemas import SchemaGenerator


@swagger_auto_schema(method='get', auto_schema=None)
@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=format),
            'images': reverse('image-list', request=request, format=format),
            'jobs': reverse('job-list', request=request, format=format),
            'classifications': reverse(
                'classification-list', request=request, format=format
            ),
            'models': reverse('mlmodel-list', request=request, format=format),
            'researcher-requests': reverse(
                'researcherrequest-list', request=request, format=format
            ),
        }
    )


schema_view = get_schema_view(
    openapi.Info(title='Moth Classifier API', default_version='v1',),
    urlconf='api.api_urls',
    public=True,
    generator_class=SchemaGenerator,
)

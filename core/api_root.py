from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse


class CustomAPIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            "companies": reverse("companies:api-root", request=request, format=format),
            "financial": reverse("financial:api-root", request=request, format=format),
        })

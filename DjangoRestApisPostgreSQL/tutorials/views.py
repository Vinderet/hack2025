from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Tutorial
from django.core import serializers
import json

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User  # Импорт модели User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


@api_view(["GET", "POST", "DELETE"])
def tutorial_list(request):
    if request.method == "GET":
        tutorials = Tutorial.objects.all()
        tutorials_json = serializers.serialize("json", tutorials)
        return JsonResponse(json.loads(tutorials_json), safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        tutorial = Tutorial(
            title=data.get("title", ""),
            description=data.get("description", ""),
            published=data.get("published", False),
        )
        tutorial.save()
        return JsonResponse(
            {
                "id": tutorial.id,
                "title": tutorial.title,
                "description": tutorial.description,
                "published": tutorial.published,
            },
            status=status.HTTP_201_CREATED,
        )

    elif request.method == "DELETE":
        Tutorial.objects.all().delete()
        return JsonResponse(
            {"message": "All tutorials were deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def tutorial_detail(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse(
            {"message": "The tutorial does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        tutorial_json = serializers.serialize("json", [tutorial])
        return JsonResponse(json.loads(tutorial_json)[0]["fields"], safe=False)

    elif request.method == "PUT":
        data = json.loads(request.body)
        tutorial.title = data.get("title", tutorial.title)
        tutorial.description = data.get("description", tutorial.description)
        tutorial.published = data.get("published", tutorial.published)
        tutorial.save()
        return JsonResponse(
            {
                "id": tutorial.id,
                "title": tutorial.title,
                "description": tutorial.description,
                "published": tutorial.published,
            }
        )

    elif request.method == "DELETE":
        tutorial.delete()
        return JsonResponse(
            {"message": "Tutorial was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET"])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)
    tutorials_json = serializers.serialize("json", tutorials)
    return JsonResponse(json.loads(tutorials_json), safe=False)

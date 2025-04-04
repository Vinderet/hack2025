from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    tutorial_list,
    tutorial_detail,
    tutorial_list_published,
)

urlpatterns = [
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/tutorials/", tutorial_list, name="tutorial_list"),
    path("api/tutorials/<int:pk>/", tutorial_detail, name="tutorial_detail"),
    path(
        "api/tutorials/published/",
        tutorial_list_published,
        name="tutorial_list_published",
    ),
]

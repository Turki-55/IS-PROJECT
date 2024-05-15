from django.urls import path
from .views import UserRegisterView,UserEditView

urlpatterns=[
    path("register/", UserRegisterView.as_view(), name="register"),
    path("editprofile/", UserEditView.as_view(), name="edit_profile"),
]
from django.urls import path
from taskweb import views
urlpatterns=[
    path("signup",views.SignUp.as_view(),name="register")
]
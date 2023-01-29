from django.urls import path
from todoweb import views
urlpatterns=[
    path("signup",views.SignUp.as_view(),name="register"),
    path("",views.loginview.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="home"),
    path("task/add/",views.TaskCreateView.as_view(),name="task-add"),
    path("task/all/",views.TasklistView.as_view(),name="task-list"),
    path("task/details/<int:id>",views.TaskDetailView.as_view(),name="task-detail"),
    path("task/remove/<int:id>",views.TaskDeleteView.as_view(),name="task-delete"),
    path("task/Change/<int:id>",views.TaskEditView.as_view(),name="task-edit"),
    path("signout",views.LogoutView.as_view(),name="signout")
]
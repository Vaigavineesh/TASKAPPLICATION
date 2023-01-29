from django.shortcuts import render,redirect
from django.views.generic import View
from todoweb.forms import Regform,loginform,Taskform,TaskEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Tasks
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

class SignUp(View):
    def get(self,request,*args,**kw):
        form=Regform()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kw):
        form=Regform(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect("signin")
        else:
            return render(request,"register.html",{"form":form})
# Create your views here.
class loginview(View):
    def get(self,request,*args,**kw):
        form=loginform()
        return render(request,"login.html",{"form":form})   
    def post(self,request,*args,**kw):
        form=loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            wd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=wd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class LogoutView(View):
    def get(self,request,*args,**kw):
        logout(request)
        return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kw):
        return render(request,"index.html")
        
@method_decorator(signin_required,name="dispatch")
class TaskCreateView(View):
    def get(self,request,*args,**kw):
        form=Taskform()
        return render(request,"task-add.html",{"form":form})

    def post(self,request,*args,**kw):
        form=Taskform(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            print("saved")
            return redirect("task-add")
        else:
            return render(request,"task-add.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class TasklistView(View):
    def get(self,request,*args,**kw):
        qs=Tasks.objects.filter(user=request.user).order_by("-created_date")
        return render(request,"task-list.html",{"tasks":qs})
@method_decorator(signin_required,name="dispatch")
class TaskDetailView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Tasks.objects.get(id=id)
        return render(request,"task-detail.html",{"tasks":qs})
@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Tasks.objects.filter(id=id).delete()
        return redirect("task-list")
@method_decorator(signin_required,name="dispatch")
class TaskEditView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        obj=Tasks.objects.get(id=id)
        form=TaskEditForm(instance=obj)
        return render(request,"task-edit.html",{"form":form})
    def post(self,request,*args,**kw):
        id=kw.get("id")
        obj=Tasks.objects.get(id=id) 
        form=TaskEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect("task-list")
        else:
            return render(request,"task-edit.html",{"form":form})




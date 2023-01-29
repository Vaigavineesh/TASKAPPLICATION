from django.shortcuts import render
from django.views.generic import View

class SignUp(View):
    def get(request,*args,**kw):
        return render(request,"register.html")
# Create your views here.

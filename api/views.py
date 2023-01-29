from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializer import Taskserializer,Userserializer
from api.models import Tasks
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
class Taskview(APIView):
    def get(self,request,*args,**kw):
        qs=Tasks.objects.all()
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kw):
        serializer=Taskserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (data=serializer.data)
        else:
            return Response(data=serializer.errors)
#localhost:8000/tasks/1/

class TaskDetailview(APIView):

    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=Taskserializer(qs,many=False)
        return Response(data=serializer.data)
    def delete(self,request,*args,**kw):
        id=kw.get("id")
        qs=Tasks.objects.get(id=id).delete()
        return Response(data="deleted")
    def put(self,request,*args,**kw):
        id=kw.get("id")
        qs=Tasks.objects.get(id=id)
        serializer=Taskserializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response (data=serializer.data)
        else:
            return Response(data=serializer.errors)

class Taskviewset(ViewSet):
    def list(self,request,*args,**kw):
        qs=Tasks.objects.all()
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=Taskserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=Taskserializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Tasks.objects.get(id=id).delete()
        return Response(data="deleted")
    def udate(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=Taskserializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response (data=serializer.data)
        else:
            return Response(data=serializer.errors)


class Taskmodelviewset(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Taskserializer
    queryset=Tasks.objects.all()
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    def list(self,request,*args,**kw):
        qs=Tasks.objects.filter(user=request.user)
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["get"],detail=False)
    def finished_tasks(self,request,*aegs,**kw):
        qs=Tasks.objects.filter(status=True)
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["get"],detail=False)
    def pending_tasks(self,request,*aegs,**kw):
        qs=Tasks.objects.filter(status=False)
        serializer=Taskserializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["POST"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        Tasks.objects.filter(id=id).update(status=True)
        return Response(data="status udated")
# Create your views here.
class UsermodelViewset(ModelViewSet):
    serializer_class=Userserializer
    queryset=User.objects.all()
    def create(self, request, *args, **kwargs):
        serializer=Userserializer(data=request.data)
        if serializer.is_valid():
            usr=User.objects.create_user(**serializer.validated_data)
            serializer=Userserializer(usr,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        

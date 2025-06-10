import uuid

from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from makevideo.models import TaskModel
from makevideo.pagination import CustomPagination
from makevideo.serializers import TaskSerializer
from makevideo.tasks import generate_video, delete_tasks


class MakeVideoViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            user=request.user
            text = request.data.get('text')
            title = request.data.get('title')
            if text is None or title is None:
                data = {
                    "success": False,
                    "message":"please is enter valid data"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            task=TaskModel.objects.create(user=user,text=text,title=title)
            print("hi")
            generate_video.delay(str(task.useduuid))
            taskdata=TaskSerializer(task).data
            print(taskdata)
            data={
                "success": True,
                "task": taskdata,
                "message": "task created successfully, please wait few minutes."
            }
            return  Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            data={
                "success": False,
                "message": "Something went wrong, please try again later."
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

class TasksModelListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user=self.request.user
        return TaskModel.objects.filter(user=user).order_by('-updated_at')

class TasksModelSuccessListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user=self.request.user
        return TaskModel.objects.filter(user=user,status="SUCCESS").order_by('-updated_at')

class TasksModelPendingListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user=self.request.user
        return TaskModel.objects.filter(user=user,status="PENDING").order_by('-updated_at')

class TasksModelFailureListView(ListAPIView):
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        user=self.request.user
        return TaskModel.objects.filter(user=user,status="FAILURE").order_by('-updated_at')

class DeleteTaskView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        useduuid = request.data.get('useduuid')
        taskuuid=uuid.UUID(useduuid)
        user=request.user
        if not TaskModel.objects.filter(useduuid=taskuuid,user=user).exists():
            data = {
                "success": False,
                "message": "Task does not exist"
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            task=TaskModel.objects.get(useduuid=taskuuid,user=user)
            if task.status=="FAILURE":
                task.delete()
                data = {
                    "success": True,
                    "message": "Task deleted successfully"
                }
                return Response(data,status=status.HTTP_200_OK)
            if task.status=="PENDING":
                data={
                    "success": False,
                    "message": "Cant delete pending task"
                }
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            useduuid=str(task.useduuid)
            delete_tasks.delay(useduuid)
            task.delete()
            data={
                "success": True,
                "message": "Task deleted successfully"
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={
                "success": False,
                "message": "Something went wrong, please try again later."
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


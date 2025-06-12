import uuid

from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from makevideo.models import TaskModel, VoiceModel, BackGroundModel
from makevideo.pagination import CustomPagination
from makevideo.serializers import TaskSerializer, BackGroundSerializer, VoiceSerializer
from makevideo.tasks import generate_video, delete_tasks


class MakeVideoViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            user=request.user
            text = request.data.get('text')
            title = request.data.get('title')
            voice = request.data.get('voice')
            bg_video_url = request.data.get('bg_video_url')
            if not VoiceModel.objects.filter(voice=voice).exists():
                data={
                    "success": False,
                    "message":"Invalid Voice"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if not BackGroundModel.objects.filter(video_url=bg_video_url).exists():
                data={
                    "success": False,
                    "message":"Invalid Back Ground Video URL"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            speed = request.data.get('speed')
            if text is None or title is None:
                data = {
                    "success": False,
                    "message":"please is enter valid data"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            if speed is None or speed < 0.5 or speed > 2:
                data = {
                    "success": False,
                    "message":"please is enter valid data"
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            task=TaskModel.objects.create(user=user,text=text,title=title,voice=voice,bg_video_url=bg_video_url,speed=speed)

            generate_video.delay(str(task.useduuid))
            taskdata=TaskSerializer(task).data
            print(taskdata)
            data={
                "success": True,
                "task": taskdata,
                "message": "task created successfully, check history."
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


class GetAllBackgroundModelView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        data=BackGroundSerializer(BackGroundModel.objects.all(),many=True).data
        data={
            "success": True,
            "data": data,
        }
        return Response(data,status=status.HTTP_200_OK)
class GetVoiceModelView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        data=VoiceSerializer(VoiceModel.objects.all(),many=True).data
        data={
            "success": True,
            "data": data,
        }
        return Response(data,status=status.HTTP_200_OK)


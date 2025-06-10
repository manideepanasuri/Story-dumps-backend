from django.urls import path

from .views import *

urlpatterns = [
    path('upload-audio/', MakeVideoViews.as_view(), name='upload-audio'),
    path('get-all-tasks/',TasksModelListView.as_view(), name='get-all-tasks'),
    path('get-success-tasks/', TasksModelSuccessListView.as_view(), name='get-success-tasks'),
    path('get-pending-tasks/', TasksModelPendingListView.as_view(), name='get-pending-tasks'),
    path('get-failure-tasks/', TasksModelFailureListView.as_view(), name='get-failure-tasks'),
    path('delete-task/',DeleteTaskView.as_view(), name='delete-task'),

]

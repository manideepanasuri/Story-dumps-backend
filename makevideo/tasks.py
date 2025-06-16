import uuid

import requests
from celery import shared_task

from brainrot.settings import GENERATE_VIDEO_URL, GENERATE_VIDEO_SECRET

from makevideo.helpers import delete_file_from_minio
from makevideo.models import TaskModel


@shared_task
def generate_video(useduuid:str):
    taskuuid=uuid.UUID(useduuid)
    task=TaskModel.objects.get(useduuid=taskuuid)
    useduuid=str(task.useduuid)
    text=task.text
    try:
        send_data={
            "text": text,
            "voice":str(task.voice),
            "speed":float(task.speed),
            "bg_video_url":str(task.bg_video_url),
            "useduuid":str(useduuid),
        }
        headers = {
            "access-token": GENERATE_VIDEO_SECRET,
            "Content-Type": "application/json"
        }
        response=requests.post(GENERATE_VIDEO_URL,json=send_data,headers=headers)
        response.raise_for_status()
        data=response.json()
        data=data["data"]
        task.status="SUCCESS"
        task.percentage = 100
        task.video_url=data["video_url"]
        task.audio_url=data["audio_url"]
        task.thumbnail_url=data["thumbnail_url"]
        task.ass_url=data["ass_url"]
        task.save()
    except Exception as e:
        task.status="FAILURE"
        task.percentage=100
        task.save()
        print(e)

@shared_task
def delete_tasks(useduuid:str):
    audio_path = f"audio/{useduuid}.wav"
    video_path = f"videos/{useduuid}.mp4"
    ass_path = f"ass/{useduuid}.ass"
    thumbnail_path = f"thumbnail/{useduuid}.jpg"
    delete_file_from_minio(audio_path)
    delete_file_from_minio(video_path)
    delete_file_from_minio(ass_path)
    delete_file_from_minio(thumbnail_path)

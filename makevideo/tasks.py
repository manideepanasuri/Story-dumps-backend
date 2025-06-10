import uuid

from celery import shared_task

from makevideo.helpers import get_audio_from_text, transcribe_audio_with_whisper, generate_ass_file, generate_video_url, \
    generate_thumbnail_url, delete_file_from_minio
from makevideo.models import TaskModel


@shared_task
def generate_video(useduuid:str):
    taskuuid=uuid.UUID(useduuid)
    task=TaskModel.objects.get(useduuid=taskuuid)
    useduuid=str(task.useduuid)
    text=task.text
    try:
        audio_url=get_audio_from_text(text,useduuid)
        task.percentage=33
        task.save()
        subtitles_array=transcribe_audio_with_whisper(audio_url,"base")
        ass_url=generate_ass_file(subtitles_array,useduuid)
        task.percentage = 66
        task.save()
        video_url=generate_video_url(audio_url,ass_url,useduuid)
        thumbnail_url=generate_thumbnail_url(video_url,useduuid)
        task.status="SUCCESS"
        task.percentage = 100
        task.video_url=video_url
        task.audio_url=audio_url
        task.thumbnail_url=thumbnail_url
        task.ass_url=ass_url
        task.save()
        print(video_url)
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

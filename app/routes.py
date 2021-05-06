import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from rq import Queue

from app.database import get_queue
from app.models import Status
from app.schemas import ResponseTaskID, ResponseTaskStatus
from app.tasks import resize_image

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    '/tasks', status_code=status.HTTP_201_CREATED, response_model=ResponseTaskID
)
def upload_image(
    file: UploadFile = File(...), queue: Queue = Depends(get_queue)
) -> ResponseTaskID:
    logger.info(f'Received file {file.filename} of type {file.content_type}')
    if not file.content_type.startswith('image'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported content type, image is expected',
        )

    job = queue.enqueue(resize_image, file.file)

    logger.info(f'Added task with id {job.id}')
    logger.info(f'Tasks in queue: {len(queue)}')

    return ResponseTaskID(id=job.id)


@router.get(
    '/tasks/{task_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseTaskStatus,
)
def check_status(task_id: str, queue: Queue = Depends(get_queue)) -> ResponseTaskStatus:
    job = queue.fetch_job(task_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )
    return ResponseTaskStatus(
        id=task_id, status=Status.from_job_status(job.get_status())
    )


@router.get(
    '/tasks/{task_id}/image',
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
)
def get_image(
    task_id: str, size: str, queue: Queue = Depends(get_queue)
) -> StreamingResponse:
    job = queue.fetch_job(task_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )
    if job.get_status() != 'finished':
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Task not ready or failed'
        )
    images = job.result
    if size not in images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect size'
        )
    return StreamingResponse(images[size], media_type='image/png')

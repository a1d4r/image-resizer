import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from app.models import Status
from app.settings import settings


def test_upload_image(client: TestClient, image_file):
    files = {'file': ('image.png', image_file, 'image/png')}
    response = client.post('/tasks', files=files)
    assert response.status_code == 201
    assert 'id' in response.json()


def test_upload_wrong_format(client: TestClient):
    with open('files/not_an_image.txt', 'r') as f:
        files = {'file': f}
        response = client.post('/tasks', files=files)
    assert response.status_code == 400


def test_check_status(client: TestClient, job_id: str):
    response = client.get(f'/tasks/{job_id}')
    assert response.status_code == 200
    assert response.json() == {'id': job_id, 'status': 'DONE'}


def test_check_status_invalid_id(client: TestClient):
    response = client.get('/tasks/aboba')
    assert response.status_code == 404


def test_get_original_image(client: TestClient, job_id: str, image_file: io.BytesIO):
    response = client.get(f'/tasks/{job_id}/image', params={'size': 'original'})
    assert response.status_code == 200

    stored_image = Image.open(image_file)
    received_image = Image.open(io.BytesIO(response.content))
    assert not ImageChops.difference(stored_image, received_image).getbbox()


@pytest.mark.parametrize('size', settings.IMAGE_SIZES)
def test_get_resized_image(client: TestClient, job_id: str, size: int):
    response = client.get(f'/tasks/{job_id}/image', params={'size': str(size)})
    assert response.status_code == 200

    received_image = Image.open(io.BytesIO(response.content))
    assert received_image.size == (size, size)


def test_get_image_invalid_id(client: TestClient):
    response = client.get('/tasks/aboba', params={'size': 'original'})
    assert response.status_code == 404


@pytest.mark.parametrize(
    'input,expected',
    [
        ('queued', Status.WAITING),
        ('started', Status.IN_PROGRESS),
        ('finished', Status.DONE),
        ('failed', Status.FAILED),
    ],
)
def test_rq_status_response(input: str, expected: str):
    assert Status.from_job_status(input) == expected

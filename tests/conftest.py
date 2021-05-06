import io

import pytest
from fakeredis import FakeStrictRedis
from fastapi.testclient import TestClient
from rq import Queue

from app.database import get_queue
from app.main import app
from app.tasks import resize_image

queue = Queue(connection=FakeStrictRedis(), is_async=False)


def get_test_queue() -> Queue:
    return queue


@pytest.fixture(scope='session')
def client():
    app.dependency_overrides[get_queue] = get_test_queue
    yield TestClient(app)


@pytest.fixture(scope='session')
def image_file():
    with open('files/image.png', 'rb') as f:
        yield f


@pytest.fixture(scope='session')
def job_id(image_file):
    image_file.seek(0)
    job = queue.enqueue(resize_image, io.BytesIO(image_file.read()))
    image_file.seek(0)
    return job.id

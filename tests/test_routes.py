import pytest

from app import create_app
from app.models import Poll, PollVote, Story
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'The Teenage Years' in response.data


def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About The Teenage Years' in response.data


def test_non_existent_route(client):
    assert client.get('/non-existent').status_code == 404


@pytest.mark.parametrize('path', ['/stories', '/story/new', '/polls', '/quiz'])
def test_pages_load(client, path):
    assert client.get(path).status_code == 200


def test_create_story(client, app):
    response = client.post('/story/new', data={'title': 'Hi', 'content': 'Text'})
    assert response.status_code == 302
    with app.app_context():
        story = Story.query.one()
        assert story.author == 'Anonymous'


def test_create_poll_and_vote_once(client, app):
    response = client.post('/polls', data={'question': 'Best?', 'options': 'A, B, ,C'})
    assert response.status_code == 302
    with app.app_context():
        poll = Poll.query.one()
        assert [o.option_text for o in poll.options] == ['A', 'B', 'C']
        poll_id, option_id = poll.id, poll.options[0].id

    client.post(f'/poll/{poll_id}', data={'option': option_id})
    client.post(f'/poll/{poll_id}', data={'option': option_id})  # duplicate
    with app.app_context():
        assert PollVote.query.count() == 1


def test_poll_needs_two_options(client, app):
    client.post('/polls', data={'question': 'Q?', 'options': 'only one'})
    with app.app_context():
        assert Poll.query.count() == 0


def test_vote_invalid_option(client, app):
    client.post('/polls', data={'question': 'Q?', 'options': 'A,B'})
    with app.app_context():
        poll_id = Poll.query.one().id
    client.post(f'/poll/{poll_id}', data={'option': 9999})
    with app.app_context():
        assert PollVote.query.count() == 0


# ----- image uploads -----
import io

PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32


def test_story_with_image(client, app):
    response = client.post('/story/new', content_type='multipart/form-data', data={
        'title': 'Hi', 'content': 'Text', 'image': (io.BytesIO(PNG), 'pic.png')})
    assert response.status_code == 302
    with app.app_context():
        filename = Story.query.one().image_filename
    assert filename and filename.endswith('.png')
    assert b'uploads/' + filename.encode() in client.get('/stories').data


def test_poll_with_image(client, app):
    client.post('/polls', content_type='multipart/form-data', data={
        'question': 'Q?', 'options': 'A,B', 'image': (io.BytesIO(PNG), 'pic.png')})
    with app.app_context():
        assert Poll.query.one().image_filename.endswith('.png')


def test_fake_image_rejected(client, app):
    client.post('/story/new', content_type='multipart/form-data', data={
        'title': 'Hi', 'content': 'Text', 'image': (io.BytesIO(b'not an image'), 'evil.png')})
    with app.app_context():
        assert Story.query.count() == 0


def test_wrong_extension_rejected(client, app):
    client.post('/story/new', content_type='multipart/form-data', data={
        'title': 'Hi', 'content': 'Text', 'image': (io.BytesIO(PNG), 'x.svg')})
    with app.app_context():
        assert Story.query.count() == 0

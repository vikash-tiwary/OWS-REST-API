import json
import requests
import pytest
from restapi import config
from tests.factories import post as post_factory
from tests.testutils import db

@pytest.fixture
def expected_header_data():
    headers = {
        'Content-Type': "application/json"
    }

    return headers

@pytest.fixture
def post_id():
    """Return a fake product id for testing."""
    return 1

@pytest.fixture
def post_data():
    data={
        "id":1,
        "title":'title',
        "description":'description'
    }
    return data

@pytest.fixture
def update_data():
    data={
        "title":'title',
        "description":'description'
    }
    return data

def post_items(posts):
    """Convert language objects to dicts."""
    return [po.to_dict() for po in posts]

@db.test_schema
def test_create_post(client,post_data,expected_header_data,post_id):
    """
    Test function to create post details
    """
    existing_post = post_factory.PostFactory.build(id=post_id)
    db.seed_models(existing_post)
    response=client.post("/post",data=json.dumps(post_data),headers=expected_header_data)
    response_body = json.loads(response.data.decode())
    assert 200==response.status_code
    # assert response_body=={
    #     "id":1,
    #     "title":'title',
    #     "description":'description'
    # }

@db.test_schema
def test_get_all_post(client):
    """
    Test function to get all post from post
    """
    posts = post_factory.PostFactory.build_batch(3)
    db.seed_models(posts)
    expected_payload = json.dumps( post_items(posts))
    response = client.get("/post")
    assert 200==response.status_code
    assert response.data.decode('utf-8') == expected_payload

def get_id_post(posts):
    for post in posts:
        if post['id']=='4':
            return post


@db.test_schema
def test_get_post(client):
    """
    Test function to get post of one id from  post
    """
    posts = post_factory.PostFactory.build_batch(3)
    db.seed_models(posts)
    post=get_id_post(post_items(posts))
    expected_payload = json.dumps(post)
    response = client.get("/post/4")
    posts=response.data.decode('utf-8')
    assert 200==response.status_code
    assert response.data.decode('utf-8') == expected_payload

@db.test_schema
def test_update_post(client,update_data,expected_header_data):
    """
    Test case to update pust details
    """

    response=client.put("/post/1",data=json.dumps(update_data),headers=expected_header_data)
    #response_body = json.loads(response.data.decode())
    assert 200==response.status_code
    # assert response_body=={
    #     "title":'title',
    #     "description":'description'
    # }

@db.test_schema
def test_delete_post(client):
    """
    Test case to delete post
    """
    response=client.delete("/post/1")

    assert 200==response.status_code

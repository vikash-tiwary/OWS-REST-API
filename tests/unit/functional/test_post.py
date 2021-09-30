import json
import requests
import pytest
from restapi import config

@pytest.fixture
def expected_header_data():
    headers = {
        'Content-Type': "application/json"
    }

    return headers


@pytest.fixture
def post_data():
    data={
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
    
def test_create_post(client,post_data,expected_header_data):
    """
    Test function to create post details
    """
    
    response = client.post("/post",data=json.dumps(post_data),headers=expected_header_data)
    assert 200==response.status_code

def test_get_all_post(client):
    """
    Test function to get all post from post
    """
    response = client.get("/post")
    assert 200==response.status_code

def test_get_post(client):
    """
    Test function to get post of one id from  post
    """
    response = client.get("/post/1")
    
    assert 200==response.status_code

def test_update_post(client,update_data,expected_header_data):
    """
    Test case to update pust details
    """

    response=client.put("/post/1",data=json.dumps(update_data),headers=expected_header_data)

    assert 200==response.status_code

def test_delete_post(client):
    """
    Test case to delete post
    """
    response=client.delete("/post/17")

    assert 200==response.status_code

import json
import requests
import pytest


headers = {
    'Content-Type': "application/json"
}

@pytest.fixture
def get_data():
    required_data={
        "id": 1,
        "title": "title-t",
        "description": "description-t"
    }
    return required_data


@pytest.fixture
def post_data():
    data={
        "title":'title',
        "description":'description'
    }
    return data
    

def test_create_post(post_data):
    """
    Test function to create post details
    """
    
    response = requests.post("http://192.168.0.103:5000/post",json=json.dumps(post_data),headers=headers)
    assert 200==response.status_code



def test_get_all_post():
    """
    Test function to get all post from post
    """
    response = requests.get("http://192.168.0.103:5000/post")
    json_data = json.loads(response.text)
    print(json_data)
    assert 200==response.status_code

def test_get_post(get_data):
    """
    Test function to get post of one id from  post
    """
    response = requests.get("http://192.168.0.103:5000/post/1")
    json_data = json.loads(response.text)
    assert get_data== json_data
    assert 200==response.status_code

def test_update_post():
    """
    Test case to update pust details
    """
    data={ 
        "title":"title2",
        "description":"description2"
    }

    response=requests.put("http://192.168.0.103:5000/post/1",json=json.dumps(data),headers=headers)

    assert 200==response.status_code

def test_delete_post():
    """
    Test case to delete post
    """
    response=requests.delete("http://192.168.0.103:5000/post/17")

    assert 200==response.status_code

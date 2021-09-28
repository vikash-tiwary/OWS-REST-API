from restapi.models import post


def get_post(id=None):
    return post.Post.get_post(id)


def create_post(post_data):
    return post.Post.create_post(post_data)

def update_post(post_data,id):
    return post.Post.update_post(post_data,id)

def delete_post(id):
    return post.Post.delete_post(id)


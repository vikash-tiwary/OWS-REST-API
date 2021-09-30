"""Application Handlers.

Requests are redirected to handlers, which are responsible for getting
information from the URL and passing it down to the logic layer. The way
each layer talks to each other is through Response objects which defines the
type status of the data and the data itself.

Please note: the Orchard uses the term handlers over views as convention
for clarity

See:
    oto.response for more details.
"""


from flask import g, jsonify, request
from owsresponse import response
from owsresponse.adaptors.flask import flaskify
from restapi import config
from restapi.api import app
from restapi.logic import hello
from restapi.logic import ows_post

# @app.route("/", methods=["GET"])
# def hello_world():
#     """Hello World with an optional GET param "name"."""
#     name = request.args.get("name", "")
#     return flaskify(hello.say_hello(name))


# @app.route("/<username>", methods=["GET"])
# def hello_world_username(username):
#     """Hello World on /<username>.

#     Args:
#         username (str): the user's username.
#     """
#     return flaskify(hello.say_hello(username))


# @app.route(config.HEALTH_CHECK, methods=["GET"])
# def health():
#     """Check the health of the application."""
#     return jsonify({"status": "ok"})


# @app.errorhandler(500)
# def exception_handler(error):
#     """Handle error when uncaught exception is raised.

#     Default exception handler.
#     Note: Exception will also be sent to Sentry if config.SENTRY is set.

#     Returns:
#         flask.Response: A 500 response with JSON 'code' & 'message' payload.
#     """
#     message = (
#         "The server encountered an internal error "
#         "and was unable to complete your request."
#     )
#     g.log.exception(error)
#     return flaskify(response.create_fatal_response(message))


# import pdb;pdb.set_trace()

@app.route('/post/<int:id>',methods=['GET'])
def get_post(id):
    """Fetch all of the possible meta language options."""
    headers = {'Cache-Control': 'max-age=86400'}
    
    return flaskify(ows_post.get_post(id), headers)

@app.route('/post',methods=['GET'])
def get_all_post():
    """Fetch all of the possible meta language options."""
    headers = {'Cache-Control': 'max-age=86400'}
    
    return flaskify(ows_post.get_post(), headers)

@app.route('/post',methods=['POST'])
def create_post():
    """Create a new post.

    Returns:
        flask.Response: on successful creation of the prouct, returns a 201
            with a JSON representation of the created post.
    """
    # headers_response = flask_request.verify_grass_headers(request)
    # if not headers_response:
    #     return flaskify(headers_response)

    post_data = request.get_json()
    return flaskify(ows_post.create_post(post_data))

@app.route('/post/<int:id>',methods=['PUT'])
def update_post(id):
    """Update an existing post details.

    Returns:
        flask.Response: on successful, 200 status with JSON body.
    """

    post_data = request.get_json()
    return flaskify(ows_post.update_post(post_data,id))


@app.route('/post/<int:id>',methods=['DELETE'])
def delete_post(id):
    """Delete an existing post details.

    Returns:
        flask.Response: on successful, 200 status with JSON body.
    """

    return flaskify(ows_post.delete_post(id))




######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Recommendation Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Recommendation
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Recommendation
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW Recommendation
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Create a Recommendation
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to Create a Recommendation...")
    check_content_type("application/json")

    recommendation = Recommendation()
    # Get the data from the request and deserialize it
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    recommendation.deserialize(data)

    # Save the new Recommendation to the database
    recommendation.create()
    app.logger.info("Recommendation with new id [%s] saved!", recommendation.id)

    # Return the location of the new Recommendation
    # Todo: uncomment this code when get_recommendations is implemented
    # location_url = url_for("get_recommendations", recommendation_id=recommendation.id, _external=True)

    location_url = "unknown"

    return (
        jsonify(recommendation.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["PUT"])
def update_recommendations(recommendation_id):
    """Update a Recommendation

    This endpoint will update a Recommendation based on the body that is posted
    """
    app.logger.info("Request to update recommendation with id: %s", recommendation_id)

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{recommendation_id}' was not found.",
        )

    data = request.get_json()
    if data is None:
        abort(status.HTTP_400_BAD_REQUEST, "Invalid JSON body")
    recommendation.deserialize(data)
    recommendation.id = recommendation_id
    recommendation.update()

    app.logger.info("Recommendation with ID [%s] updated.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# E R R O R   H A N D L E R S
######################################################################


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors as JSON"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors as JSON"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors as JSON"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED, error="Method Not Allowed", message=message),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(415)
def unsupported_media_type(error):
    """Handle 415 Unsupported Media Type errors as JSON"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, error="Unsupported Media Type", message=message),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server Error as JSON"""
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR, error="Internal Server Error", message=message),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type) -> None:
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )

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
and Delete Recommendations
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Recommendation, RecommendationType
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            {
                "name": "Recommendation REST API Service",
                "version": "1.0.0",
                "paths": {
                    "list": "/recommendations",
                },
            }
        ),
        status.HTTP_200_OK,
    )


######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendations list")

    recommendations = []

    # Parse any arguments from the query string
    recommendation_type = request.args.get("recommendation_type")
    source_product_id = request.args.get("source_product_id")

    if recommendation_type:
        app.logger.info("Find by recommendation_type: %s", recommendation_type)
        # convert string value to enum e.g. "cross_sell" -> RecommendationType.CROSS_SELL
        try:
            type_enum = RecommendationType[recommendation_type.upper()]
        except KeyError:
            abort(
                status.HTTP_400_BAD_REQUEST,
                f"Invalid recommendation_type: {recommendation_type}",
            )
        recommendations = Recommendation.find_by_type(type_enum)
    elif source_product_id:
        app.logger.info("Find by source_product_id: %s", source_product_id)
        recommendations = Recommendation.find_by_source_product_id(
            int(source_product_id)
        )
    else:
        app.logger.info("Find all")
        recommendations = Recommendation.all()

    results = [r.serialize() for r in recommendations]
    app.logger.info("Returning %d recommendations", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ A RECOMMENDATION
######################################################################
# query to recommendations by ID
@app.route("/recommendations/<int:recommendation_id>", methods=["GET"])
def get_recommendations(recommendation_id):
    """
    Retrieve a single Recommendation

    This endpoint will return a Recommendation based on its id
    """
    app.logger.info(
        "Request to Retrieve a recommendation with id [%s]", recommendation_id
    )

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{recommendation_id}' was not found.",
        )

    app.logger.info("Returning recommendation: %s", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# CREATE A NEW RECOMMENDATION
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
    data = request.get_json()
    app.logger.info("Processing: %s", data)
    recommendation.deserialize(data)

    recommendation.create()
    app.logger.info("Recommendation with new id [%s] saved!", recommendation.id)

    location_url = url_for(
        "get_recommendations", recommendation_id=recommendation.id, _external=True
    )
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
    """
    Update a Recommendation

    This endpoint will update a Recommendation based the body that is posted
    """
    app.logger.info(
        "Request to Update a recommendation with id [%s]", recommendation_id
    )
    check_content_type("application/json")

    recommendation = Recommendation.find(recommendation_id)
    if not recommendation:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{recommendation_id}' was not found.",
        )

    data = request.get_json()
    app.logger.info("Processing: %s", data)
    recommendation.deserialize(data)

    recommendation.update()

    app.logger.info("Recommendation with ID: %d updated.", recommendation.id)
    return jsonify(recommendation.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendation_id>", methods=["DELETE"])
def delete_recommendations(recommendation_id):
    """
    Delete a Recommendation

    This endpoint will delete a Recommendation based the id specified in the path
    """
    app.logger.info(
        "Request to Delete a recommendation with id [%s]", recommendation_id
    )

    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        app.logger.info("Recommendation with ID: %d found.", recommendation.id)
        recommendation.delete()

    app.logger.info("Recommendation with ID: %d delete complete.", recommendation_id)
    return {}, status.HTTP_204_NO_CONTENT


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


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

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
TestRecommendation API Service Test Suite
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Recommendation, RecommendationType
from .factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/recommendations"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_recommendation = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_recommendation.serialize())
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_recommendation = response.get_json()
        self.assertEqual(
            new_recommendation["source_product_id"],
            test_recommendation.source_product_id,
        )
        self.assertEqual(
            new_recommendation["recommended_product_id"],
            test_recommendation.recommended_product_id,
        )
        self.assertEqual(
            new_recommendation["recommendation_type"],
            test_recommendation.recommendation_type.value,
        )

        # # Uncomment this code when get_recommendations is implemented
        # # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_recommendation = response.get_json()
        # self.assertEqual(
        #     new_recommendation["source_product_id"],
        #     test_recommendation.source_product_id,
        # )
        # self.assertEqual(
        #     new_recommendation["recommended_product_id"],
        #     test_recommendation.recommended_product_id,
        # )
        # self.assertEqual(
        #     new_recommendation["recommendation_type"],
        #     test_recommendation.recommendation_type.value,
        # )

    ######################################################################
    #  T E S T   U P D A T E   E N D P O I N T
    ######################################################################

    def test_update_recommendation(self):
        """It should update an existing Recommendation and return 200"""
        # Create and persist a recommendation
        recommendation = RecommendationFactory()
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)

        # Build updated data with a different recommendation_type
        original_type = recommendation.recommendation_type.value
        new_type = next(
            t.value for t in RecommendationType if t.value != original_type
        )
        updated_data = {
            "source_product_id": recommendation.source_product_id,
            "recommended_product_id": recommendation.recommended_product_id,
            "recommendation_type": new_type,
        }

        resp = self.client.put(
            f"/recommendations/{recommendation.id}",
            json=updated_data,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["id"], recommendation.id)
        self.assertEqual(data["source_product_id"], updated_data["source_product_id"])
        self.assertEqual(
            data["recommended_product_id"], updated_data["recommended_product_id"]
        )
        self.assertEqual(data["recommendation_type"], new_type)

    def test_update_recommendation_not_found(self):
        """It should return 404 when updating a non-existent Recommendation"""
        payload = {
            "source_product_id": 1,
            "recommended_product_id": 2,
            "recommendation_type": "cross_sell",
        }
        resp = self.client.put(
            "/recommendations/999",
            json=payload,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_recommendation_bad_json(self):
        """It should return 400 when the PUT request body is invalid JSON"""
        # Create and persist a recommendation so the ID exists
        recommendation = RecommendationFactory()
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)

        resp = self.client.put(
            f"/recommendations/{recommendation.id}",
            data="this-is-not-json",
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

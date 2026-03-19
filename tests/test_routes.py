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
from service.models import db, Recommendation
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

    def test_delete_recommendation(self):
        """It should Delete an existing Recommendation"""
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_recommendation = response.get_json()
        recommendation_id = new_recommendation["id"]

        response = self.client.delete(f"{BASE_URL}/{recommendation_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        deleted_recommendation = Recommendation.find(recommendation_id)
        self.assertIsNone(deleted_recommendation)

    def test_delete_recommendation_not_found(self):
        """It should return 404 when deleting a Recommendation that does not exist"""
        response = self.client.delete(f"{BASE_URL}/999999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recommendation_missing_field(self):
        """It should not Create a Recommendation with missing data"""
        test_recommendation = {"source_product_id": 1, "recommended_product_id": 2}
        response = self.client.post(BASE_URL, json=test_recommendation)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recommendation_invalid_type(self):
        """It should not Create a Recommendation with invalid recommendation type"""
        test_recommendation = {
            "source_product_id": 1,
            "recommended_product_id": 2,
            "recommendation_type": "invalid_type",
        }
        response = self.client.post(BASE_URL, json=test_recommendation)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """It should return 405 when using an unsupported method"""
        response = self.client.put(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_recommendation_no_json(self):
        """It should not Create a Recommendation with non-JSON data"""
        response = self.client.post(
            BASE_URL, data="not json", content_type="text/plain"
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_recommendation_no_content_type(self):
        """It should not Create a Recommendation without a Content-Type header"""
        test_recommendation = {
            "source_product_id": 1,
            "recommended_product_id": 2,
            "recommendation_type": "cross_sell",
        }
        response = self.client.post(
            BASE_URL,
            data='{"source_product_id": 1, "recommended_product_id": 2, "recommendation_type": "cross_sell"}',
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

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

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

    # Utility function to bulk create recommendations
    ############################################################
    def _create_recommendations(self, count: int = 1) -> list:
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test recommendation",
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the home page and return service metadata"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data["name"], "Recommendation REST API Service")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["paths"]["list"], "/recommendations")

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_recommendation(self):
        """It should Get a single Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(
            data["source_product_id"], test_recommendation.source_product_id
        )
        self.assertEqual(
            data["recommended_product_id"], test_recommendation.recommended_product_id
        )
        self.assertEqual(
            data["recommendation_type"], test_recommendation.recommendation_type.name
        )

    def test_get_recommendation_not_found(self):
        """It should not Get a Recommendation that's not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_recommendation(self):
        """It should Update an existing Recommendation"""
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)
        new_recommendation["recommendation_type"] = RecommendationType.UP_SELL.name
        response = self.client.put(
            f"{BASE_URL}/{new_recommendation['id']}", json=new_recommendation
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()
        self.assertEqual(
            updated_recommendation["recommendation_type"],
            RecommendationType.UP_SELL.name,
        )

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
Test cases for Recommendation Model
"""

# pylint: disable=duplicate-code
import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import Recommendation, RecommendationType, DataValidationError, db
from .factories import RecommendationFactory
from unittest.mock import patch

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestRecommendation(TestCase):
    """Test Cases for Recommendation Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_recommendation(self):
        """It should Create a Recommendation and assert that it exists"""
        recommendation = Recommendation(
            source_product_id=1,
            recommended_product_id=2,
            recommendation_type=RecommendationType.CROSS_SELL,
        )
        self.assertEqual(str(recommendation), "<Recommendation id=[None]>")
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.source_product_id, 1)
        self.assertEqual(recommendation.recommended_product_id, 2)
        self.assertEqual(
            recommendation.recommendation_type, RecommendationType.CROSS_SELL
        )

    def test_add_a_recommendation(self):
        """It should Create a Recommendation and add it to the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        recommendation = RecommendationFactory()
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        recommendation.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(recommendation.id)
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)

    def test_read_a_recommendation(self):
        """It should Read a Recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        # Fetch it back
        found_recommendation = Recommendation.find(recommendation.id)
        self.assertEqual(found_recommendation.id, recommendation.id)
        self.assertEqual(
            found_recommendation.source_product_id, recommendation.source_product_id
        )
        self.assertEqual(
            found_recommendation.recommended_product_id,
            recommendation.recommended_product_id,
        )
        self.assertEqual(
            found_recommendation.recommendation_type, recommendation.recommendation_type
        )

    def test_update_a_recommendation(self):
        """It should Update a Recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        logging.debug(recommendation)
        self.assertIsNotNone(recommendation.id)
        # Change it and save it
        recommendation.recommendation_type = RecommendationType.UP_SELL
        original_id = recommendation.id
        recommendation.update()
        self.assertEqual(recommendation.id, original_id)
        self.assertEqual(recommendation.recommendation_type, RecommendationType.UP_SELL)
        # Fetch it back and make sure the id hasn't changed but the data did change
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].id, original_id)
        self.assertEqual(
            recommendations[0].recommendation_type, RecommendationType.UP_SELL
        )

    def test_update_no_id(self):
        """It should not Update a Recommendation with no id"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        self.assertRaises(DataValidationError, recommendation.update)

    def test_delete_a_recommendation(self):
        """It should Delete a Recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertEqual(len(Recommendation.all()), 1)
        # Delete the recommendation and make sure it isn't in the database
        recommendation.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_list_all_recommendations(self):
        """It should List all Recommendations in the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        # Create 5 Recommendations
        for _ in range(5):
            recommendation = RecommendationFactory()
            recommendation.create()
        # See if we get back 5 recommendations
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 5)

    def test_serialize_a_recommendation(self):
        """It should serialize a Recommendation"""
        recommendation = RecommendationFactory()
        data = recommendation.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], recommendation.id)
        self.assertIn("source_product_id", data)
        self.assertEqual(data["source_product_id"], recommendation.source_product_id)
        self.assertIn("recommended_product_id", data)
        self.assertEqual(
            data["recommended_product_id"], recommendation.recommended_product_id
        )
        self.assertIn("recommendation_type", data)
        self.assertEqual(
            data["recommendation_type"], recommendation.recommendation_type.name
        )

    def test_deserialize_a_recommendation(self):
        """It should de-serialize a Recommendation"""
        data = RecommendationFactory().serialize()
        recommendation = Recommendation()
        recommendation.deserialize(data)
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.source_product_id, data["source_product_id"])
        self.assertEqual(
            recommendation.recommended_product_id, data["recommended_product_id"]
        )
        self.assertEqual(
            recommendation.recommendation_type.name, data["recommendation_type"]
        )

    def test_deserialize_missing_data(self):
        """It should not deserialize a Recommendation with missing data"""
        data = {"source_product_id": 1}
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_recommendation_type(self):
        """It should not deserialize a bad recommendation_type attribute"""
        data = RecommendationFactory().serialize()
        data["recommendation_type"] = "invalid_type"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    # Additional test cases
    def test_find_by_source_product_id(self):
        """It should Find Recommendations by source_product_id"""
        recommendations = RecommendationFactory.create_batch(3)
        # create all with same source_product_id
        source_id = recommendations[0].source_product_id
        for rec in recommendations:
            rec.source_product_id = source_id
            rec.create()

        found = Recommendation.find_by_source_product_id(source_id)
        self.assertEqual(len(list(found)), 3)

    def test_create_db_error(self):
        """It should raise DataValidationError on create DB failure"""
        recommendation = RecommendationFactory()
        with patch(
            "service.models.db.session.commit", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, recommendation.create)

    def test_update_db_error(self):
        """It should raise DataValidationError on update DB failure"""
        recommendation = RecommendationFactory()
        recommendation.create()
        with patch(
            "service.models.db.session.commit", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, recommendation.update)

    def test_delete_db_error(self):
        """It should raise DataValidationError on delete DB failure"""
        recommendation = RecommendationFactory()
        recommendation.create()
        with patch(
            "service.models.db.session.delete", side_effect=Exception("DB error")
        ):
            self.assertRaises(DataValidationError, recommendation.delete)

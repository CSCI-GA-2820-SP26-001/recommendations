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
Test cases for Pet Model
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

    def test_create_recommendation(self):
        """It should create a Recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        found = Recommendation.all()
        self.assertEqual(len(found), 1)
        data = Recommendation.find(recommendation.id)
        self.assertEqual(data.source_product_id, recommendation.source_product_id)
        self.assertEqual(
            data.recommended_product_id, recommendation.recommended_product_id
        )
        self.assertEqual(data.recommendation_type, recommendation.recommendation_type)

    def test_update_a_recommendation(self):
        """It should update a Recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()

        recommendation.recommendation_type = RecommendationType.UP_SELL
        recommendation.update()

        found = Recommendation.find(recommendation.id)
        self.assertEqual(found.recommendation_type, RecommendationType.UP_SELL)

    def test_delete_a_recommendation(self):
        """It should delete a Recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()

        recommendation.delete()
        found = Recommendation.find(recommendation.id)
        self.assertIsNone(found)

    def test_find_recommendation(self):
        """It should find a Recommendation by id"""
        recommendation = RecommendationFactory()
        recommendation.create()

        found = Recommendation.find(recommendation.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, recommendation.id)

    def test_list_all_recommendations(self):
        """It should return all Recommendations"""
        rec1 = RecommendationFactory()
        rec2 = RecommendationFactory()
        rec1.create()
        rec2.create()

        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 2)

    def test_deserialize_with_missing_data(self):
        """It should not deserialize a Recommendation with missing data"""
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, {})

    def test_deserialize_with_none(self):
        """It should not deserialize a Recommendation with bad data"""
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, None)

    def test_deserialize_with_invalid_enum(self):
        """It should not deserialize a Recommendation with invalid recommendation_type"""
        recommendation = Recommendation()
        bad_data = {
            "source_product_id": 1,
            "recommended_product_id": 2,
            "recommendation_type": "not_real",
        }
        self.assertRaises(DataValidationError, recommendation.deserialize, bad_data)

    def test_serialize_a_recommendation(self):
        """It should serialize a Recommendation"""
        recommendation = RecommendationFactory()
        data = recommendation.serialize()
        self.assertEqual(data["source_product_id"], recommendation.source_product_id)
        self.assertEqual(
            data["recommended_product_id"], recommendation.recommended_product_id
        )
        self.assertEqual(
            data["recommendation_type"], recommendation.recommendation_type.value
        )

    def test_repr_of_recommendation(self):
        """It should return the string representation of a Recommendation"""
        recommendation = RecommendationFactory()
        self.assertIn("Recommendation", repr(recommendation))
        self.assertIn(str(recommendation.source_product_id), repr(recommendation))

    def test_find_recommendation_not_found(self):
        """It should return None if a Recommendation is not found"""
        recommendation = Recommendation.find(0)
        self.assertIsNone(recommendation)

    @patch("service.models.db.session.commit")
    def test_create_raises_data_validation_error(self, mock_commit):
        """It should raise DataValidationError when create fails"""
        mock_commit.side_effect = Exception("db boom")
        recommendation = RecommendationFactory()
        self.assertRaises(DataValidationError, recommendation.create)

    @patch("service.models.db.session.commit")
    def test_update_raises_data_validation_error(self, mock_commit):
        """It should raise DataValidationError when update fails"""
        recommendation = RecommendationFactory()
        recommendation.create()
        mock_commit.side_effect = Exception("db boom")
        self.assertRaises(DataValidationError, recommendation.update)

    @patch("service.models.db.session.commit")
    def test_delete_raises_data_validation_error(self, mock_commit):
        """It should raise DataValidationError when delete fails"""
        recommendation = RecommendationFactory()
        recommendation.create()
        mock_commit.side_effect = Exception("db boom")
        self.assertRaises(DataValidationError, recommendation.delete)

    def test_deserialize_with_bad_attribute(self):
        """It should not deserialize a Recommendation with a bad attribute"""
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, "not a dict")

    # Todo: Add your test cases here...

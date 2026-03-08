"""
Models for Recommendation

All of the models are stored in this module
"""

import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    source_product_id = db.Column(db.Integer, nullable=False)
    recommended_product_id = db.Column(db.Integer, nullable=False)
    recommendation_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Recommendation id={self.id}>"

    def create(self):
        """
        Creates a Recommendation in the database
        """
        logger.info("Creating recommendation")
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Recommendation in the database
        """
        logger.info("Updating recommendation")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Recommendation from the data store"""
        logger.info("Deleting recommendation")
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
"""Serializes a Recommendation into a dictionary"""
    return {
    "id": self.id,
    "source_product_id": self.source_product_id,
    "recommended_product_id": self.recommended_product_id,
    "recommendation_type": self.recommendation_type,
    "created_at": self.created_at.isoformat() if self.created_at else None,}


def deserialize(self, data):
    """
    Deserializes a Recommendation from a dictionary

    Args:
        data (dict): A dictionary containing the recommendation data
    """
    try:
        self.source_product_id = data["source_product_id"]
        self.recommended_product_id = data["recommended_product_id"]
        self.recommendation_type = data["recommendation_type"]
        self.created_at = data.get("created_at")
    except AttributeError as error:
        raise DataValidationError("Invalid attribute: " + error.args[0]) from error
    except KeyError as error:
        raise DataValidationError(
            "Invalid Recommendation: missing " + error.args[0]
        ) from error
    except TypeError as error:
        raise DataValidationError(
            "Invalid Recommendation: body of request contained bad or no data "
            + str(error)
        ) from error
    return self
    

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Recommendations in the database"""
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Recommendation by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_product_id(cls, product_id):
        """Returns all Recommendations for a given source product id"""
        logger.info("Processing product_id query for %s ...", product_id)
        return cls.query.filter(cls.source_product_id == product_id).all()
   
    @classmethod
    def find_by_recommendation_type(cls, recommendation_type):
        """Returns all Recommendations for a given recommendation type"""
        logger.info(
            "Processing recommendation_type query for %s ...",
            recommendation_type,
        )
        return cls.query.filter(
            cls.recommendation_type == recommendation_type
        ).all()
    
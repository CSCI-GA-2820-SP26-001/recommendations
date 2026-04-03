"""
Models for Recommendation

All of the models are stored in this module
"""

import logging
import enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class RecommendationType(enum.Enum):
    """Enumeration of valid recommendation types"""

    CROSS_SELL = "cross_sell"
    UP_SELL = "up_sell"
    ACCESSORY = "accessory"


class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """

    ##################################################
    # Table Schema
    ##################################################
    __tablename__ = "recommendations"

    #Reject Duplicate Recommendation Relationships
    __table_args__ = (
        db.UniqueConstraint(
            "source_product_id",
            "recommended_product_id",
            "recommendation_type",
            name="uq_recommendation",
        ),
        db.CheckConstraint(
            "source_product_id != recommended_product_id",
            name="ck_no_self_recommendation",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    source_product_id = db.Column(db.Integer, nullable=False)
    recommended_product_id = db.Column(db.Integer, nullable=False)
    recommendation_type = db.Column(db.Enum(RecommendationType), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Recommendation id=[{self.id}]>"

    def create(self):
        """Creates a Recommendation to the database"""
        logger.info(
            "Creating recommendation source=%s -> recommended=%s",
            self.source_product_id,
            self.recommended_product_id,
        )
        self.id = None
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """Updates a Recommendation to the database"""
        logger.info("Saving recommendation id=%s", self.id)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Recommendation from the data store"""
        logger.info("Deleting recommendation id=%s", self.id)
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
            "recommendation_type": self.recommendation_type.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.source_product_id = data["source_product_id"]
            self.recommended_product_id = data["recommended_product_id"]
            try:
                self.recommendation_type = RecommendationType[
                    data["recommendation_type"].upper()
                ]
            except KeyError as error:
                raise DataValidationError(
                    "Invalid recommendation_type: " + str(data["recommendation_type"])
                ) from error
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

    #query recommendation by ID
    @classmethod
    def find(cls, by_id):
        """Finds a Recommendation by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_type(cls, recommendation_type: RecommendationType) -> list:
        """Returns all Recommendations with the given type

        Args:
            recommendation_type (RecommendationType): the type to match
        """
        logger.info("Processing type query for %s ...", recommendation_type)
        return cls.query.filter(cls.recommendation_type == recommendation_type)

    @classmethod
    def find_by_source_product_id(cls, source_product_id: int) -> list:
        """Returns all Recommendations with the given source_product_id

        Args:
            source_product_id (int): the source product id to match
        """
        logger.info("Processing source_product_id query for %s ...", source_product_id)
        return cls.query.filter(cls.source_product_id == source_product_id)

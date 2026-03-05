"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    id = factory.Sequence(lambda n: n)
    source_product_id = factory.Sequence(lambda n: n + 1)
    recommended_product_id = factory.LazyAttribute(lambda obj: obj.source_product_id + 1)
    recommendation_type = FuzzyChoice(RecommendationType)
    created_at = factory.Faker("date_time")
    updated_at = factory.Faker("date_time")
    # Todo: Add your other attributes here...

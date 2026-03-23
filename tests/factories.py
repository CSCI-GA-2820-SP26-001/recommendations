"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, RecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake recommendations for testing"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    id = None
    source_product_id = factory.Sequence(lambda n: n + 1)
    recommended_product_id = factory.LazyAttribute(
        lambda obj: obj.source_product_id + 1
    )
    recommendation_type = FuzzyChoice(choices=list(RecommendationType))

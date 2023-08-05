import unittest

from featureflow.user import User
from featureflow.evaluate import Evaluate

from .test_helpers import feature

DEFAULT_FEATURE_VARIANT = 'off'


class EvaluateTest(unittest.TestCase):
    """Tests for Featureflow.Evaluate"""
    def test_disabled(self):
        """Evaluate returns defaultFeatureVariant (off) for disabled feature"""
        f = feature(enabled=False)
        evaluate = Evaluate(TestClient(), f, User())

        self.assertEqual(evaluate.value(), f['offVariantKey'])
        self.assertEqual(evaluate._evaluated_variant, f['offVariantKey'])

    def test_default_rule(self):
        """Evaluate returns one of variantSplits keys for feature default rule"""
        f = feature()
        values = [v['variantKey'] for v in f['rules'][0]['variantSplits']]

        evaluate = Evaluate(TestClient(), f, User())

        self.assertIn(evaluate._evaluated_variant, values)
        self.assertIn(evaluate.value(), values)


class TestClient:
    def __init__(self):
        self.events_client = self._events_client()

    def _events_client(self):
        """docstring for __init__"""
        class Ev:
            def __init__(self):
                pass

            def evaluate(self, x):
                return x
        return Ev()

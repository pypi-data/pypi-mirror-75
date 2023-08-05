from datetime import date
import unittest

from featureflow.condition import Condition
from .test_helpers import values, fake


class ConditionTest(unittest.TestCase):
    """Tests for Featureflow.Condition"""
    def test_equals(self):
        """Test 'equals' operator for all supported types"""
        operator = 'equals'
        vals = [fake.word(), fake.random_int(0, 100), fake.date()]
        # Equals case
        for val in vals:
            condition = Condition(operator=operator, values=values(value=val))
            self.assertTrue(condition.evaluate(val))

        # Not equals case
        for val in vals:
            condition = Condition(operator=operator, values=values())
            self.assertFalse(condition.evaluate(val))

    def test_contains(self):
        """Test 'contains' operator for strings"""
        operator = 'contains'

        val = fake.word()

        length = len(val) // 2

        substr = val[fake.random_int(0, length):fake.random_int(1, length)]

        condition = Condition(operator=operator, values=values(value=substr))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertFalse(condition.evaluate(val))

    def test_starts_with(self):
        """Test 'startsWith' operator for strings"""
        operator = 'startsWith'

        val = fake.word()

        length = len(val) // 2

        substr = val[0:fake.random_int(1, length)]

        condition = Condition(operator=operator, values=values(value=substr))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertFalse(condition.evaluate(val))

    def test_ends_with(self):
        """Test 'endsWith' operator for strings"""
        operator = 'endsWith'

        val = fake.word()

        length = len(val) // 2

        substr = val[fake.random_int(0, length):]

        condition = Condition(operator=operator, values=values(value=substr))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertFalse(condition.evaluate(val))

    def test_matches(self):
        """Test 'matches' operator for strings"""
        operator = 'matches'

        val = fake.word()

        length = len(val) // 2

        substr = val[fake.random_int(0, length):fake.random_int(1, length)]
        regex = ".*{}.*".format(substr)

        condition = Condition(operator=operator, values=values(value=regex))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertFalse(condition.evaluate(val))

    def test_in(self):
        """Test 'in' operator for strings"""
        operator = 'in'

        val = fake.word()

        condition = Condition(operator=operator, values=values(value=val))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertFalse(condition.evaluate(val))

    def test_not_in(self):
        """Test 'notIn' operator for strings"""
        operator = 'notIn'

        val = fake.word()

        condition = Condition(operator=operator, values=values(value=val))
        self.assertFalse(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=fake.word()))
        self.assertTrue(condition.evaluate(val))

    def test_before(self):
        """Test 'before' operator for strings"""
        operator = 'before'

        val = fake.date()

        val_true = fake.date(end_datetime=date.fromisoformat(val))
        val_false = fake.date_between(start_date=date.fromisoformat(val)).isoformat()

        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

    def test_after(self):
        """Test 'after' operator for strings"""
        operator = 'after'

        val = fake.date()

        val_true = fake.date_between(start_date=date.fromisoformat(val)).isoformat()
        val_false = fake.date(end_datetime=date.fromisoformat(val))

        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

    def test_greater_than(self):
        """Test 'greaterThan' operator for strings"""
        operator = 'greaterThan'

        val = fake.random_int(0, 100)

        val_true = val - fake.random_int(1, val)
        val_false = val + fake.random_int(0, 100)

        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

    def test_less_than(self):
        """Test 'lessThan' operator for strings"""
        operator = 'lessThan'

        val = fake.random_int(0, 100)

        val_true = val + fake.random_int(1, val)
        val_false = val - fake.random_int(0, 100)

        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

    def test_greater_than_or_equal(self):
        """Test 'greaterThanOrEqual' operator for strings"""
        operator = 'greaterThanOrEqual'

        val = fake.random_int(0, 100)

        val_true = val - fake.random_int(1, val)
        val_false = val + fake.random_int(1, 100)

        # Greater
        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Equal
        condition = Condition(operator=operator, values=values(value=val))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

    def test_less_than_or_equal(self):
        """Test 'lessThanOrEqual' operator for strings"""
        operator = 'lessThanOrEqual'

        val = fake.random_int(0, 100)

        val_true = val + fake.random_int(1, val)
        val_false = val - fake.random_int(1, 100)

        # Less
        condition = Condition(operator=operator, values=values(value=val_true))
        self.assertTrue(condition.evaluate(val))

        # Equal
        condition = Condition(operator=operator, values=values(value=val))
        self.assertTrue(condition.evaluate(val))

        # Not
        condition = Condition(operator=operator, values=values(value=val_false))
        self.assertFalse(condition.evaluate(val))

from faker import Faker

fake = Faker()

OPERATORS = (
    'equals',
    'contains',
    'startsWith',
    'endsWith',
    'matches',
    'in',
    'notIn',
    'before',
    'after',
    'greaterThan',
    'greaterThanOrEqual',
    'lessThan',
    'lessThanOrEqual'
)


def feature(enabled=True, default_rule=True, conditions=True, operator=None):
    """Generates feature structure like parsed JSON from server"""

    return {
        'key': fake.word(),
        'variantSalt': fake.word(),
        'enabled': enabled,
        'offVariantKey': fake.word(),
        'rules': [rule(default_rule, conditions, operator)],
    }


def values(value=None, n=5):
    vals = [fake.random_int(0, 10) for _ in range(5)]

    if value is not None:
        return [value] + vals
    else:
        return vals


def rule(default_rule=True, conditions=True, operator=None, value=None):
    """Generates rule structure"""
    split = fake.random_int(0, 100)
    operator = operator if operator is not None else fake.random_element(elements=OPERATORS)

    return {
        'defaultRule': default_rule,
        'audience': {
            'conditions': [
                {
                    'target': fake.word(),
                    'operator': operator,
                    'values': values(value, 10),
                }
            ] if conditions else None
        } if not default_rule else None,
        'variantSplits': [
            {
                'variantKey': fake.word(),
                'split': split,
            },
            {
                'variantKey': fake.word(),
                'split': 100 - split,
            }
        ]
    }

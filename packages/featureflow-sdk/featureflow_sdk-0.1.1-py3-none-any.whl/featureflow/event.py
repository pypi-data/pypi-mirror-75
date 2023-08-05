class Event:
    def __init__(self, **event):
        """docstring for __init__"""
        self.feature_key = event.get('feature_key')
        self.evaluated_variant = event.get('evaluated_variant')
        self.expected_variant = event.get('expected_variant', None)
        self.user = event.get('user', None)

    def toJSON(self):
        """docstring for toJSON"""
        return {
            'featureKey': self.feature_key,
            'evaluatedVariant': self.evaluated_variant,
            'expectedVariant': self.expected_variant,
            'user': self.user.toJSON() if self.user is not None else None,
        }

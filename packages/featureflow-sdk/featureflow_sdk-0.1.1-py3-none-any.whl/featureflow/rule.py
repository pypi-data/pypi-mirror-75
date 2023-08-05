#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .condition import Condition


class Rule:
    def __init__(self, rule):
        """docstring for __init__"""
        self._rule = rule

    @property
    def default(self):
        return self._rule.get('defaultRule', False)

    @property
    def conditions(self):
        audience = self._rule.get('audience', {})
        return [Condition(c) for c in audience.get('conditions', [])]

    @property
    def variant_splits(self):
        return self._rule.get('variantSplits', [])

    def match(self, user):
        if self.default:
            return True

        if self.conditions is []:
            return True

        if user is None:
            return False

        attributes = user.attributes.update(user.session_attributes)

        for condition in self.conditions:
            result = False
            for attribute in attributes:
                if condition.evaluate(attribute):
                    result = True

            if not result:
                return False

        return True

    def get_variant_split_key(self, variant_value):
        """docstring for get_variant_split_key"""
        percent = 0
        for vs in self.variant_splits:
            percent += vs['split']
            if percent >= variant_value:
                return vs['variantKey']

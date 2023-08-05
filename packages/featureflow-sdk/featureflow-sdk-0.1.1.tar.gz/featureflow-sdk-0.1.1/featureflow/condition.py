#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import re


class Condition:
    def __init__(self, **args):
        """docstring for __init"""
        self.target = args.get('target', None)
        self.operator = args.get('operator', None)
        self.values = args.get('values', [])

    def evaluate(self, attribute):
        """docstring for evaluate"""
        if self.operator == "equals":
            return attribute == self.values[0]

        if self.operator == "contains" and type(attribute) == str:
            return self.values[0] in attribute

        if self.operator == "startsWith" and type(attribute) == str:
            return attribute.startswith(self.values[0])

        if self.operator == "endsWith" and type(attribute) == str:
            return attribute.endswith(self.values[0])

        if self.operator == "matches" and type(attribute) == str:
            return re.compile(self.values[0]).match(attribute) is not None

        if self.operator == "in" and type(attribute) == str:
            return attribute in self.values

        if self.operator == "notIn" and type(attribute) == str:
            return attribute not in self.values

        if self.operator == "greaterThan" and type(attribute) in [int, float]:
            return attribute > self.values[0]

        if self.operator == "lessThan" and type(attribute) in [int, float]:
            return attribute < self.values[0]

        if self.operator == "greaterThanOrEqual" and type(attribute) in [int, float]:
            return attribute >= self.values[0]

        if self.operator == "lessThanOrEqual" and type(attribute) in [int, float]:
            return attribute <= self.values[0]

        if self.operator == "after" and type(attribute) == str:
            first = datetime.fromisoformat(self.values[0])
            second = datetime.fromisoformat(attribute)
            return first > second

        if self.operator == "before" and type(attribute) == str:
            first = datetime.fromisoformat(self.values[0])
            second = datetime.fromisoformat(attribute)
            return first < second

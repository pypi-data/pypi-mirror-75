#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from .feature import Feature
from .event import Event


class Evaluate:
    DEFAULT_FEATURE_VARIANT = "off"

    def __init__(self, client, feature, user):
        """docstring for __init__"""
        self._client = client
        self._feature = Feature(feature)
        self._user = user

        self._evaluated_variant = self._calculate_variant()

    def value(self):
        """Returns value of evaluated variant"""
        self._client.events_client.evaluate([Event(feature_key=self._feature.key,
                                     evaluated_variant=self._evaluated_variant,
                                     user=self._user
                                     ).toJSON()
                               ])

        return self._evaluated_variant

    def is_(self, variant):
        """docstring for is"""
        self._client.events_client.evaluate([Event(feature_key=self._feature.key,
                                     evaluated_variant=self._evaluated_variant,
                                     expected_variant=variant,
                                     user=self._user
                                     ).toJSON()
                               ])
        return self._evaluated_variant == variant

    def isOn(self):
        """docstring for isOn"""
        return self.is_('on')

    def isOff(self):
        """docstring for isOff"""
        return self.is_('off')

    def _calculate_variant(self):
        if not self._feature.enabled:
            return self._feature.off_variant_key

        for rule in self._feature.rules:
            if rule.match(self._user):
                variant_value = self._feature.get_variant_value(self._user)
                return rule.get_variant_split_key(variant_value)

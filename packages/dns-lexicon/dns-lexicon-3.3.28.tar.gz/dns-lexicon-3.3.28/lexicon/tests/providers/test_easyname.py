"""Integration tests for EasyName"""
from unittest import TestCase

from lexicon.tests.providers.integration_tests import IntegrationTestsV2


class EasynameProviderTests(TestCase, IntegrationTestsV2):
    """TestCase for EasyName"""
    provider_name = 'easyname'
    domain = 'nigl.it'

    def _filter_post_data_parameters(self):
        return ['username', 'password']

    def _filter_headers(self):
        return ['Cookie']

    def _test_fallback_fn(self):
        return lambda x: 'placeholder_' + x if x != 'priority' else ''

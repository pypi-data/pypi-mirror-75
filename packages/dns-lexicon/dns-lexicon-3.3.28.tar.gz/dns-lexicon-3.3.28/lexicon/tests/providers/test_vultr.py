"""Integration tests for Vultr"""
from unittest import TestCase

import pytest

from lexicon.tests.providers.integration_tests import IntegrationTestsV1


# Hook into testing framework by inheriting unittest.TestCase and reuse
# the tests which *each and every* implementation of the interface must
# pass, by inheritance from define_tests.TheTests
# TODO: migrate to IntegrationTestsV2 and its extended test suite
class VultrProviderTests(TestCase, IntegrationTestsV1):
    """TestCase for Vultr"""
    provider_name = 'vultr'
    domain = 'capsulecd.com'

    def _filter_headers(self):
        return ['API-Key']

    # TODO: enable the skipped tests
    @pytest.mark.skip(reason="new test, missing recording")
    def test_provider_when_calling_update_record_should_modify_record_name_specified(self):
        return

import time

import pytest

from main import Cache


def test_cache_add_and_check():
    """
    Test that a new key is not found, but is cached after first check.
    """
    cache = Cache()
    cache.clear_cache()  # Ensure clean state

    query_type = "query"
    query = "Test Query"
    # First check: should not exist
    assert cache.check_if_key_exists(query_type, query) is False
    # Second check: should exist
    assert cache.check_if_key_exists(query_type, query) is True


def test_cache_normalization():
    """
    Test that queries are normalized (case and whitespace) before caching.
    """
    cache = Cache()
    cache.clear_cache()

    query_type = "query"
    query1 = "  Test Query  "
    query2 = "test query"
    # Add first
    assert cache.check_if_key_exists(query_type, query1) is False
    # Second, normalized, should be found
    assert cache.check_if_key_exists(query_type, query2) is True


def test_cache_clear():
    """
    Test that clearing the cache removes all keys.
    """
    cache = Cache()
    cache.clear_cache()

    query_type = "query"
    query = "something unique"
    assert cache.check_if_key_exists(query_type, query) is False
    assert cache.check_if_key_exists(query_type, query) is True
    cache.clear_cache()
    # After clearing, should not exist
    assert cache.check_if_key_exists(query_type, query) is False


# Optionally, test expiry (requires time.sleep, so usually skipped in fast test runs)


@pytest.mark.skip(reason="Slow test: tests cache expiry")
def test_cache_expiry():
    """
    Test that cache entries expire after the set TTL.
    """
    cache = Cache()
    cache.clear_cache()
    query_type = "query"
    query = "expire me"
    # Manually set a short expiry for this test
    key = cache.create_key(query_type, query)
    cache.cache.set(key, True, expire=2)  # 2 seconds
    assert cache.check_if_key_exists(query_type, query) is True
    time.sleep(3)
    # Should be expired now
    assert cache.check_if_key_exists(query_type, query) is False

import logging

import pytest

from app_data import *
from main import *


def test_class_init():
    """
    Testing generation of class related values on class initialization
    """
    TestIdiot = Idiot()
    assert TestIdiot.first_name is None
    assert TestIdiot.last_name is None
    assert TestIdiot.full_name is None
    assert TestIdiot.email is None
    assert TestIdiot.intro is None

    assert TestIdiot.random_include_name == 1 or TestIdiot.random_include_name == 2
    assert (
        TestIdiot.random_include_greeting >= 1
        and TestIdiot.random_include_greeting <= 4
    )
    assert TestIdiot.include_greeting == bool(TestIdiot.include_greeting)
    assert TestIdiot.include_name == bool(TestIdiot.include_name)


def test_gen_name():
    """
    Testing name generation functionality
    """
    TestIdiot = Idiot()
    TestIdiot.gen_first_name()
    TestIdiot.gen_last_name()
    TestIdiot.gen_full_name()
    assert TestIdiot.full_name is not None
    assert TestIdiot.full_name == str(TestIdiot.full_name)

    test_first_name = TestIdiot.full_name.split(" ")[0]
    assert test_first_name in first_names

    test_last_name = TestIdiot.full_name.split(" ")[-1]
    assert test_last_name in last_names


def test_gen_email():
    """
    Testing email generation functionality
    """
    TestIdiot = Idiot()
    TestIdiot.gen_first_name()
    TestIdiot.gen_last_name()
    TestIdiot.gen_full_name()
    TestIdiot.gen_email()

    possible_email_domains = ["gmai1", "yahooo", "hotmai1", "ao1", "qmail"]
    hasDomain = [d for d in possible_email_domains if (d in TestIdiot.email)]
    connectors = ["-", "_", ".", ""]
    hasConnector = [c for c in connectors if (c in TestIdiot.email)]
    assert TestIdiot.email is not None
    assert hasDomain != []
    assert hasConnector != []
    assert ".com" in TestIdiot.email
    assert "@" in TestIdiot.email


def test_first_gen_query():
    """
    Testing to ensure full range of query options (i.e. first one is accessible)
    """
    TestIdiot = Idiot()
    TestIdiot.gen_first_name()
    TestIdiot.gen_last_name()
    TestIdiot.gen_full_name()
    TestIdiot.gen_email()
    TestIdiot.random_query = 1

    expected_output = "do you have any shoes in size 16? I can fit into a woman's size 19 if that helps"
    actual_output = TestIdiot.gen_query()
    assert expected_output == actual_output


def test_last_gen_query():
    """
    Testing to ensure full range of query options (i.e. last one is accessible)
    """
    TestIdiot = Idiot()
    TestIdiot.gen_first_name()
    TestIdiot.gen_last_name()
    TestIdiot.gen_full_name()
    TestIdiot.gen_email()
    # Last query
    TestIdiot.random_query = 75

    expected_output = "is Fitzpatrick a family name?"
    actual_output = TestIdiot.gen_query()
    assert expected_output == actual_output


@pytest.fixture(autouse=True)
def patch_external_calls(mocker):
    """
    Automatically patch external calls for all tests in this module.
    """
    # Patch the submission and notification functions
    mocker.patch("main.submit_annyoing_msg")
    mocker.patch("main.ping_ntfy")
    mocker.patch("main.ping_discord")
    # Patch Cache.clean_cache to avoid side effects
    mocker.patch.object(Cache, "clean_cache")
    # Patch print to capture output
    mocker.patch("builtins.print")


def test_time_to_annoy_unique_generation(mocker):
    """
    Test that time_to_annoy generates unique query, first name, and last name,
    and calls the submission and notification functions.
    """
    # Patch Cache to use a fresh cache for this test
    cache = Cache()
    cache.clear_cache()
    mocker.patch("main.Cache", return_value=cache)

    # Patch Idiot to control randomness if needed
    # mocker.patch("main.Idiot", wraps=Idiot)  # Optionally, to control names/queries

    # Run the function
    time_to_annoy()

    # Check that submission and notification functions were called
    from main import ping_discord, ping_ntfy, submit_annyoing_msg

    assert submit_annyoing_msg.called, "submit_annyoing_msg should be called"
    assert ping_ntfy.called, "ping_ntfy should be called"
    assert ping_discord.called, "ping_discord should be called"

    # Check that the cache now contains the generated query, first name, and last name
    # (You could extract these from the call args if you want to be thorough)


def test_time_to_annoy_no_exceptions(mocker):
    """
    Test that time_to_annoy does not raise exceptions under normal conditions.
    """
    cache = Cache()
    cache.clear_cache()
    mocker.patch("main.Cache", return_value=cache)
    mocker.patch("main.submit_annyoing_msg")
    mocker.patch("main.ping_ntfy")
    mocker.patch("main.ping_discord")
    mocker.patch.object(Cache, "clean_cache")
    mocker.patch("builtins.print")

    try:
        time_to_annoy()
    except Exception as e:
        pytest.fail(f"time_to_annoy raised an exception: {e}")


def test_time_to_annoy_logging(mocker, caplog):
    """
    Test that time_to_annoy logs expected info.
    """
    cache = Cache()
    cache.clear_cache()
    mocker.patch("main.Cache", return_value=cache)
    mocker.patch("main.submit_annyoing_msg")
    mocker.patch("main.ping_ntfy")
    mocker.patch("main.ping_discord")
    mocker.patch.object(Cache, "clean_cache")
    mocker.patch("builtins.print")

    with caplog.at_level(logging.INFO):
        time_to_annoy()
        # Check for expected log messages
        assert any("Unique query found after" in m for m in caplog.messages)
        assert any("Unique first name found after" in m for m in caplog.messages)
        assert any("Unique last name found after" in m for m in caplog.messages)
        assert any("Query sent by" in m for m in caplog.messages)

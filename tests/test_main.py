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
    TestIdiot.gen_name()
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
    TestIdiot.gen_name()
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
    TestIdiot.gen_name()
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
    TestIdiot.gen_name()
    TestIdiot.gen_email()
    # Last query
    TestIdiot.random_query = 40

    expected_output = (
        "if i supplied the leather... could you make the shoes out of it..."
    )
    actual_output = TestIdiot.gen_query()
    assert expected_output == actual_output


# TODO
def test_gen_intro():
    # TestIdiot = Idiot()
    pass

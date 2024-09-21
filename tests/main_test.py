import pytest

from data import *
from main import *


def test_class_init():
  TestIdiot = Idiot()
  assert TestIdiot.first_name == None
  assert TestIdiot.last_name == None
  assert TestIdiot.full_name == None
  assert TestIdiot.email == None
  assert TestIdiot.intro == None

  assert TestIdiot.random_include_name == 1 or TestIdiot.random_include_name == 2
  assert TestIdiot.random_include_greeting >= 1 and TestIdiot.random_include_greeting <= 4
  assert TestIdiot.include_greeting == bool(TestIdiot.include_greeting)
  assert TestIdiot.include_name == bool(TestIdiot.include_name)

def test_gen_name():
  TestIdiot = Idiot()
  TestIdiot.gen_name()
  assert TestIdiot.full_name is not None
  assert TestIdiot.full_name == str(TestIdiot.full_name)

  test_first_name = TestIdiot.full_name.split(" ")[0]
  assert test_first_name in first_names

  test_last_name = TestIdiot.full_name.split(" ")[-1]
  assert test_last_name in last_names

# Todo
def test_gen_email():
  TestIdiot = Idiot()
  pass

def test_gen_intro():
  TestIdiot = Idiot()
  pass

def test_gen_query():
  TestIdiot = Idiot()
  pass

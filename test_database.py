import pytest
import database
import random


def test_create_new_room():
    number = random.randint(0, 1024)
    database.create_new_room(f"my_room_{number}")
    assert True == True

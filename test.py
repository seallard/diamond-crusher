from utils import *


def test_direction_base_cases():

    assert get_direction((1,0))  == "WEST"
    assert get_direction((-1,0)) == "EAST"
    assert get_direction((0,1))  == "NORTH"
    assert get_direction((0,-1)) == "SOUTH"

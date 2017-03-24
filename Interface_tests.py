"""
Interface_tests.

Terje Russka
"""

from Game import Interface


def test_Data_normal():
    """
    Testib koodi kui tekstifail on tavalisel kujul.

    :return:
    """
    test_normal = Interface.Data("data_normal.txt")
    assert test_normal.Get_Games() == "6"
    assert test_normal.Get_Comp_Stats() == ["11", "16", "4", "1", "0", "10"]
    assert test_normal.Get_User_Stats() == ["13", "9", "16", "19", "20", "10"]


def test_Data_Empty():
    """
    Testib koodi kui tekstifail on tühi.

    :return:
    """
    test_empty = Interface.Data("data_empty.txt")
    assert test_empty.Get_Games() == "0"
    assert test_empty.Get_Comp_Stats() == []
    assert test_empty.Get_User_Stats() == []

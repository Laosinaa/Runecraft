"""
Interface_tests.

Terje Russka
"""

from Game import grid_skele


def test_Runes():
    """
    Testib kas elemendid saavad õiged atribuudid.

    :return:
    """
    all_types = [
        "Fire", "Nature", "Law", "Blood",
        "Water", "Air", "Mind", "Chaos",
        "Soul", "Body", "Cosmic", "Essence"
    ]
    test = grid_skele.Runes("test")
    test.give_type()
    assert test.check_type() in all_types
    assert test.rune_ID() == "test"
    if test.check_type() == "Essence":
        assert test.attacks == all_types.remove("Essence")
        assert test.weaknesses == []


def test_Environment():
    """
    Testib kas keskkonnad saavad õiged atribuudid.

    :return:
    """
    all_environments = ["Fire_env", "Earth_env", "Water_env", "Cosmic_env"]
    test = grid_skele.Environment("test")
    assert test.environment_check() in all_environments
    assert test.environment_id() == "test"


def test_game_runes():
    """
    Testib kas elemendid saavad ilusti arvuti ja kasutaja vahel jaotatud.

    :return:
    """
    player = grid_skele.Player()
    computer = grid_skele.Computer()
    test = grid_skele.game_runes(player, computer, 40)
    assert isinstance(test, dict)
    assert len(player.rune_IDs) == 20
    assert len(computer.rune_IDs) == 20
    assert player.rune_IDs not in computer.rune_IDs


def test_game_environments():
    """
    Testib kas luuakse mängu jaoks keskkonnad.

    :return:
    """
    test = grid_skele.game_environments(8)
    test_len = test.keys()
    assert isinstance(test, dict)
    assert len(test_len) == 8

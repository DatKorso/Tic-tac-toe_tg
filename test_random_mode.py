"""Simple test to verify RANDOM mode mechanics"""

from app.game.logic import TicTacToeGame, GameMode, Player, GameState


def test_random_mode_places_random_symbols():
    """Test that RANDOM mode places random symbols on each move"""
    game = TicTacToeGame(game_mode=GameMode.RANDOM.value)
    game.randomize_sides()

    # Make some moves
    game.make_move(0, 0)
    game.make_move(0, 1)
    game.make_move(0, 2)

    # Check that moves were made (cells are not empty)
    assert game.board[0][0] != Player.EMPTY.value
    assert game.board[0][1] != Player.EMPTY.value
    assert game.board[0][2] != Player.EMPTY.value

    # Check that symbols are X or O
    for cell in [game.board[0][0], game.board[0][1], game.board[0][2]]:
        assert cell in [Player.X.value, Player.O.value]

    print("✓ Random symbols are placed correctly")


def test_sides_assignment():
    """Test that player and AI are assigned to different sides"""
    game = TicTacToeGame(game_mode=GameMode.RANDOM.value)
    game.randomize_sides()

    # Player and AI should have different sides
    assert game.player_side != game.ai_side

    # Both sides should be X or O
    assert game.player_side in [Player.X.value, Player.O.value]
    assert game.ai_side in [Player.X.value, Player.O.value]

    print(f"✓ Player side: {game.player_side}, AI side: {game.ai_side}")


def test_winner_determination():
    """Test that winner is correctly determined based on sides"""
    game = TicTacToeGame(game_mode=GameMode.RANDOM.value)

    # Set player to X side, AI to O side
    game.player_side = Player.X.value
    game.ai_side = Player.O.value

    # Create a winning board for X
    game.board = [
        [Player.X.value, Player.X.value, Player.X.value],
        [Player.O.value, Player.EMPTY.value, Player.EMPTY.value],
        [Player.EMPTY.value, Player.EMPTY.value, Player.EMPTY.value],
    ]
    game._update_game_state()

    # X won, so player should win
    winner = game.get_actual_winner()
    assert winner == "player"
    assert game.game_state == GameState.X_WON.value

    print("✓ Winner determination works correctly")


def test_ai_loses_when_o_wins_but_ai_is_x():
    """Test that AI loses when O wins but AI represents X side"""
    game = TicTacToeGame(game_mode=GameMode.RANDOM.value)

    # Set player to O side, AI to X side
    game.player_side = Player.O.value
    game.ai_side = Player.X.value

    # Create a winning board for O
    game.board = [
        [Player.O.value, Player.O.value, Player.O.value],
        [Player.X.value, Player.EMPTY.value, Player.EMPTY.value],
        [Player.EMPTY.value, Player.EMPTY.value, Player.EMPTY.value],
    ]
    game._update_game_state()

    # O won, and player represents O, so player should win
    winner = game.get_actual_winner()
    assert winner == "player"
    assert game.game_state == GameState.O_WON.value

    print("✓ Winner is correctly determined regardless of symbol")


def test_classic_mode_unchanged():
    """Test that CLASSIC mode still works as before"""
    game = TicTacToeGame(game_mode=GameMode.CLASSIC.value)

    # In classic mode, moves use current_player
    game.make_move(0, 0)
    assert game.board[0][0] == Player.X.value  # Player X starts

    game.make_move(1, 1)
    assert game.board[1][1] == Player.O.value  # Switched to O

    print("✓ Classic mode works correctly")


if __name__ == "__main__":
    print("Testing RANDOM mode mechanics...\n")

    test_random_mode_places_random_symbols()
    test_sides_assignment()
    test_winner_determination()
    test_ai_loses_when_o_wins_but_ai_is_x()
    test_classic_mode_unchanged()

    print("\n✅ All tests passed!")

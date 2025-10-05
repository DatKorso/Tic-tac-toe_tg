"""Tic-Tac-Toe game logic implementation"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import random


class GameMode(str, Enum):
    """Game mode representation"""

    CLASSIC = "classic"  # Player knows symbols, AI uses minimax
    RANDOM = "random"  # Player doesn't know symbols, AI uses random


class Player(str, Enum):
    """Player representation"""

    X = "❌"
    O = "⭕"  # noqa: E741
    EMPTY = "⬜"


class GameState(str, Enum):
    """Game state representation"""

    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


@dataclass
class TicTacToeGame:
    """
    Tic-Tac-Toe game logic with AI opponent.

    Supports two modes:
    - CLASSIC: Player knows symbols, AI uses minimax (unbeatable)
    - RANDOM: Each move places a random symbol (X or O).
             Winner determined by which side (X or O) gets 3 in a row.
             Player and AI are assigned to sides (X or O) at game start.
    """

    board: list[list[str]] = field(
        default_factory=lambda: [[Player.EMPTY.value] * 3 for _ in range(3)]
    )
    current_player: str = Player.X.value
    game_state: str = GameState.IN_PROGRESS.value
    game_mode: str = GameMode.CLASSIC.value
    player_side: str = (
        Player.X.value
    )  # Which side (X or O) player represents in RANDOM mode
    ai_side: str = Player.O.value  # Which side (X or O) AI represents in RANDOM mode

    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board.

        In CLASSIC mode: uses current_player symbol
        In RANDOM mode: places a random symbol (X or O)

        Args:
            row: Row index (0-2)
            col: Column index (0-2)

        Returns:
            True if move was successful, False otherwise
        """
        if not self._is_valid_move(row, col):
            return False

        # In RANDOM mode, place a random symbol
        if self.game_mode == GameMode.RANDOM.value:
            symbol = random.choice([Player.X.value, Player.O.value])
            self.board[row][col] = symbol
        else:
            # In CLASSIC mode, use current_player
            self.board[row][col] = self.current_player

        self._update_game_state()

        if self.game_state == GameState.IN_PROGRESS.value:
            self._switch_player()

        return True

    def _is_valid_move(self, row: int, col: int) -> bool:
        """Check if move is valid"""
        if self.game_state != GameState.IN_PROGRESS.value:
            return False

        if not (0 <= row < 3 and 0 <= col < 3):
            return False

        return self.board[row][col] == Player.EMPTY.value

    def _switch_player(self) -> None:
        """Switch current player"""
        self.current_player = (
            Player.O.value if self.current_player == Player.X.value else Player.X.value
        )

    def _update_game_state(self) -> None:
        """Update game state after a move"""
        winner = self._check_winner()

        if winner == Player.X.value:
            self.game_state = GameState.X_WON.value
        elif winner == Player.O.value:
            self.game_state = GameState.O_WON.value
        elif self._is_board_full():
            self.game_state = GameState.DRAW.value
        else:
            self.game_state = GameState.IN_PROGRESS.value

    def get_actual_winner(self) -> str | None:
        """
        Get the actual winner based on game mode.

        In CLASSIC mode: returns "player" or "ai" based on X/O winning
        In RANDOM mode: returns "player" or "ai" based on which side won

        Returns:
            "player", "ai", "draw", or None if game in progress
        """
        if self.game_state == GameState.IN_PROGRESS.value:
            return None

        if self.game_state == GameState.DRAW.value:
            return "draw"

        # Determine which symbol won
        winning_symbol = None
        if self.game_state == GameState.X_WON.value:
            winning_symbol = Player.X.value
        elif self.game_state == GameState.O_WON.value:
            winning_symbol = Player.O.value

        if not winning_symbol:
            return None

        # In CLASSIC mode, player is always X
        if self.game_mode == GameMode.CLASSIC.value:
            return "player" if winning_symbol == Player.X.value else "ai"

        # In RANDOM mode, check which side won
        if winning_symbol == self.player_side:
            return "player"
        elif winning_symbol == self.ai_side:
            return "ai"

        return None

    def _check_winner(self) -> Optional[str]:
        """
        Check if there's a winner.

        Returns:
            Winner player symbol or None
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != Player.EMPTY.value:
                return row[0]

        # Check columns
        for col in range(3):
            if (
                self.board[0][col]
                == self.board[1][col]
                == self.board[2][col]
                != Player.EMPTY.value
            ):
                return self.board[0][col]

        # Check diagonals
        if (
            self.board[0][0]
            == self.board[1][1]
            == self.board[2][2]
            != Player.EMPTY.value
        ):
            return self.board[0][0]

        if (
            self.board[0][2]
            == self.board[1][1]
            == self.board[2][0]
            != Player.EMPTY.value
        ):
            return self.board[0][2]

        return None

    def _is_board_full(self) -> bool:
        """Check if board is full"""
        return all(cell != Player.EMPTY.value for row in self.board for cell in row)

    def get_board_string(self) -> str:
        """Get formatted board string"""
        return "\n".join("".join(cell for cell in row) for row in self.board)

    def get_display_board(self) -> list[list[str]]:
        """
        Get board for display (shows actual symbols for played moves in RANDOM mode).

        In RANDOM mode:
        - Shows real symbols (❌/⭕) for cells where moves were made
        - Player doesn't know which symbol is theirs until game ends

        Returns:
            Board with real symbols for played moves
        """
        # In CLASSIC mode or when game ended, always show actual board
        if (
            self.game_mode == GameMode.CLASSIC.value
            or self.game_state != GameState.IN_PROGRESS.value
        ):
            return self.board

        # In RANDOM mode during game: show real symbols (but player doesn't know which is theirs)
        return self.board

    def make_ai_move(self) -> tuple[int, int] | None:
        """
        Make AI move based on game mode.

        Returns:
            Tuple of (row, col) where AI made move, or None if game is over
        """
        if self.game_state != GameState.IN_PROGRESS.value:
            return None

        if self.game_mode == GameMode.RANDOM.value:
            return self._make_random_ai_move()
        else:
            return self._make_minimax_ai_move()

    def _make_random_ai_move(self) -> tuple[int, int] | None:
        """
        Make random AI move (for RANDOM mode).

        Returns:
            Tuple of (row, col) where AI made move, or None if game is over
        """
        if self.game_state != GameState.IN_PROGRESS.value:
            return None

        # Get all empty cells
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == Player.EMPTY.value:
                    empty_cells.append((row, col))

        if not empty_cells:
            return None

        # Pick random empty cell
        move = random.choice(empty_cells)
        self.make_move(move[0], move[1])
        return move

    def _make_minimax_ai_move(self) -> tuple[int, int] | None:
        """
        Make AI move using minimax algorithm (for CLASSIC mode).

        Returns:
            Tuple of (row, col) where AI made move, or None if game is over
        """
        if self.game_state != GameState.IN_PROGRESS.value:
            return None

        best_score = float("-inf")
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == Player.EMPTY.value:
                    # Try move
                    self.board[row][col] = self.current_player
                    score = self._minimax(False)
                    self.board[row][col] = Player.EMPTY.value

                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            self.make_move(best_move[0], best_move[1])
            return best_move

        return None

    def _minimax(self, is_maximizing: bool) -> float:
        """
        Minimax algorithm for AI.

        Args:
            is_maximizing: Whether current player is maximizing

        Returns:
            Score of the position
        """
        winner = self._check_winner()

        # Terminal states
        if winner == Player.O.value:  # AI wins
            return 10
        if winner == Player.X.value:  # Player wins
            return -10
        if self._is_board_full():  # Draw
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == Player.EMPTY.value:
                        self.board[row][col] = Player.O.value
                        score = self._minimax(False)
                        self.board[row][col] = Player.EMPTY.value
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == Player.EMPTY.value:
                        self.board[row][col] = Player.X.value
                        score = self._minimax(True)
                        self.board[row][col] = Player.EMPTY.value
                        best_score = min(score, best_score)
            return best_score

    def reset(self) -> None:
        """Reset game to initial state"""
        self.board = [[Player.EMPTY.value] * 3 for _ in range(3)]
        self.current_player = Player.X.value
        self.game_state = GameState.IN_PROGRESS.value
        # Keep game_mode, player_symbol and ai_symbol unchanged

    def randomize_sides(self) -> None:
        """
        Randomly assign which side (X or O) belongs to player vs AI (for RANDOM mode).
        This determines who wins if X or O gets 3 in a row.
        """
        if random.choice([True, False]):
            self.player_side = Player.X.value
            self.ai_side = Player.O.value
        else:
            self.player_side = Player.O.value
            self.ai_side = Player.X.value

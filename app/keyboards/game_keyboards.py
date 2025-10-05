"""Inline keyboards for Telegram bot"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.game.logic import TicTacToeGame


def get_game_keyboard(game: TicTacToeGame) -> InlineKeyboardMarkup:
    """
    Generate inline keyboard for the game board.

    Args:
        game: Current game instance

    Returns:
        InlineKeyboardMarkup with game buttons
    """
    keyboard = []

    # Get display board (hides symbols in RANDOM mode)
    display_board = game.get_display_board()

    for row_idx in range(3):
        row = []
        for col_idx in range(3):
            cell = display_board[row_idx][col_idx]
            # Create callback data in format "move_row_col"
            callback_data = f"move_{row_idx}_{col_idx}"

            button = InlineKeyboardButton(text=cell, callback_data=callback_data)
            row.append(button)
        keyboard.append(row)

    # Add "New Game" button below the board
    keyboard.append(
        [InlineKeyboardButton(text="🔄 Новая игра", callback_data="new_game")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_start_keyboard() -> InlineKeyboardMarkup:
    """
    Generate start menu keyboard.

    Returns:
        InlineKeyboardMarkup with start menu buttons
    """
    keyboard = [
        [InlineKeyboardButton(text="🎮 Играть с ботом", callback_data="select_mode")],
        [InlineKeyboardButton(text="ℹ️ Как играть", callback_data="how_to_play")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_mode_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Generate game mode selection keyboard.

    Returns:
        InlineKeyboardMarkup with mode selection buttons
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text="🎯 Классический режим", callback_data="mode_classic"
            )
        ],
        [InlineKeyboardButton(text="🎲 Случайный режим", callback_data="mode_random")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_start")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

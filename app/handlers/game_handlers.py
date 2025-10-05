"""Game handlers for the bot"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.game.logic import TicTacToeGame, GameState, Player, GameMode
from app.keyboards.game_keyboards import (
    get_game_keyboard,
    get_start_keyboard,
    get_mode_selection_keyboard,
)


router = Router()

# Store active games per user
games: dict[int, TicTacToeGame] = {}


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command"""
    await message.answer(
        "👋 Добро пожаловать в Крестики-Нолики!\n\n"
        "Я — непобедимый бот, использующий алгоритм minimax. "
        "Попробуй выиграть! 😎\n\n"
        "Выбери действие:",
        reply_markup=get_start_keyboard(),
    )


@router.message(Command("newgame"))
async def cmd_new_game(message: Message) -> None:
    """Handle /newgame command"""
    user_id = message.from_user.id
    game = TicTacToeGame()
    games[user_id] = game

    await message.answer(
        "🎮 Новая игра начата!\n\n"
        f"Ты играешь за {Player.X.value}\n"
        f"Бот играет за {Player.O.value}\n\n"
        "Твой ход:",
        reply_markup=get_game_keyboard(game),
    )


@router.callback_query(F.data == "select_mode")
async def callback_select_mode(callback: CallbackQuery) -> None:
    """Handle mode selection button"""
    await callback.message.edit_text(
        "🎮 Выбери режим игры:\n\n"
        "🎯 *Классический режим*\n"
        "Ты играешь за ❌, бот за ⭕\n"
        "Бот использует непобедимый алгоритм minimax\n\n"
        "🎲 *Случайный режим*\n"
        "Каждый ход ставит СЛУЧАЙНЫЙ символ (❌ или ⭕)!\n"
        "Ты узнаешь свою сторону (X или O) в начале игры.\n"
        "Если три символа твоей стороны соберутся в ряд - победа!\n"
        "Бот делает случайные ходы. Всё зависит от удачи! 🍀",
        parse_mode="Markdown",
        reply_markup=get_mode_selection_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_start")
async def callback_back_to_start(callback: CallbackQuery) -> None:
    """Handle back to start button"""
    await callback.message.edit_text(
        "👋 Добро пожаловать в Крестики-Нолики!\n\nВыбери действие:",
        reply_markup=get_start_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mode_"))
async def callback_start_game_with_mode(callback: CallbackQuery) -> None:
    """Handle game start with selected mode"""
    user_id = callback.from_user.id

    # Parse mode from callback data
    mode = callback.data.split("_")[1]  # "classic" or "random"

    # Create game with selected mode
    game = TicTacToeGame(game_mode=mode)

    if mode == GameMode.RANDOM.value:
        # Randomize sides for player
        game.randomize_sides()
        games[user_id] = game

        await callback.message.edit_text(
            "🎲 Случайный режим!\n\n"
            f"🎯 Ты играешь за сторону: {game.player_side}\n"
            f"🤖 Бот играет за сторону: {game.ai_side}\n\n"
            "⚠️ Каждый ход ставит СЛУЧАЙНЫЙ символ (❌ или ⭕)!\n"
            "Если три символа твоей стороны соберутся в ряд - ты победишь!\n"
            "Удача решает всё! 🍀\n\n"
            "Твой ход:",
            reply_markup=get_game_keyboard(game),
        )
    else:
        games[user_id] = game

        await callback.message.edit_text(
            "🎯 Классический режим!\n\n"
            f"Ты играешь за {Player.X.value}\n"
            f"Бот играет за {Player.O.value}\n\n"
            "Твой ход:",
            reply_markup=get_game_keyboard(game),
        )

    await callback.answer("Игра началась!")


@router.callback_query(F.data == "play_vs_bot")
async def callback_play_vs_bot(callback: CallbackQuery) -> None:
    """Handle play vs bot button (redirect to mode selection)"""
    await callback_select_mode(callback)


@router.callback_query(F.data == "how_to_play")
async def callback_how_to_play(callback: CallbackQuery) -> None:
    """Handle how to play button"""
    await callback.message.edit_text(
        "📖 Как играть:\n\n"
        "1️⃣ Ты ходишь первым (крестики ❌)\n"
        "2️⃣ Бот ходит вторым (нолики ⭕)\n"
        "3️⃣ Цель — собрать 3 своих символа в ряд\n"
        "   (по горизонтали, вертикали или диагонали)\n\n"
        "⚠️ Внимание: бот использует алгоритм minimax\n"
        "и практически непобедим!\n\n"
        "Удачи! 🍀",
        reply_markup=get_start_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "new_game")
async def callback_new_game(callback: CallbackQuery) -> None:
    """Handle new game button"""
    user_id = callback.from_user.id

    # Get previous game mode or default to classic
    old_game = games.get(user_id)
    game_mode = old_game.game_mode if old_game else GameMode.CLASSIC.value

    # Create new game with same mode
    game = TicTacToeGame(game_mode=game_mode)

    if game_mode == GameMode.RANDOM.value:
        game.randomize_sides()
        games[user_id] = game

        await callback.message.edit_text(
            "🎲 Новая игра (Случайный режим)!\n\n"
            f"🎯 Ты играешь за сторону: {game.player_side}\n"
            f"🤖 Бот играет за сторону: {game.ai_side}\n\n"
            "⚠️ Стороны перемешаны!\n"
            "Каждый ход ставит случайный символ.\n\n"
            "Твой ход:",
            reply_markup=get_game_keyboard(game),
        )
    else:
        games[user_id] = game

        await callback.message.edit_text(
            "� Новая игра (Классический режим)!\n\n"
            f"Ты играешь за {Player.X.value}\n"
            f"Бот играет за {Player.O.value}\n\n"
            "Твой ход:",
            reply_markup=get_game_keyboard(game),
        )

    await callback.answer("Новая игра начата!")


@router.callback_query(F.data.startswith("move_"))
async def callback_make_move(callback: CallbackQuery) -> None:
    """Handle player move"""
    user_id = callback.from_user.id

    # Get or create game
    if user_id not in games:
        games[user_id] = TicTacToeGame()

    game = games[user_id]

    # Parse move coordinates
    _, row_str, col_str = callback.data.split("_")
    row, col = int(row_str), int(col_str)

    # Check if game is over
    if game.game_state != GameState.IN_PROGRESS.value:
        await callback.answer("Игра окончена! Начни новую игру.", show_alert=True)
        return

    # Make player move
    if not game.make_move(row, col):
        await callback.answer("Неверный ход! Выбери пустую клетку.", show_alert=True)
        return

    # Check if game ended after player move
    message_text = _get_game_status_message(game)

    if game.game_state == GameState.IN_PROGRESS.value:
        # Make AI move
        ai_move = game.make_ai_move()
        if ai_move:
            message_text = _get_game_status_message(game)

    # Update board
    await callback.message.edit_text(message_text, reply_markup=get_game_keyboard(game))
    await callback.answer()


def _get_game_status_message(game: TicTacToeGame) -> str:
    """Get game status message based on game state"""
    winner = game.get_actual_winner()

    if game.game_mode == GameMode.RANDOM.value:
        # In RANDOM mode, use get_actual_winner() to determine who won
        if winner == "player":
            winning_side = game.player_side
            return f"🎉 Ты победил!\n\nТвоя сторона была {winning_side}!\nСлучайные ходы собрали три в ряд! 🍀"
        elif winner == "ai":
            losing_side = game.player_side
            winning_side = game.ai_side
            return f"😢 Ты проиграл!\n\nТвоя сторона была {losing_side}!\nБот играл за {winning_side}. Попробуй ещё раз! 💪"
        elif winner == "draw":
            return f"🤝 Ничья!\n\nТвоя сторона была {game.player_side}.\nХороша игра!"
        else:
            return "🎲 Случайный режим\n\nКаждый ход ставит случайный символ!\nТы не знаешь свою сторону.\nТвой ход:"
    else:
        # Classic mode messages
        if winner == "player":
            return f"🎉 Ты победил! {Player.X.value} выиграл!\n\nНевероятно! 🏆"
        elif winner == "ai":
            return f"😢 Ты проиграл! {Player.O.value} выиграл!\n\nПопробуй ещё раз! 💪"
        elif winner == "draw":
            return "🤝 Ничья!\n\nХороша игра!"
        else:
            return f"🎮 Игра продолжается\n\nТвой ход ({Player.X.value}):"

# Copilot Instructions for Tic-Tac-Toe Telegram Bot

## Architecture Overview

This is an **aiogram 3.x** Telegram bot with a modular architecture designed for dual-mode deployment (polling/webhook) and future scalability to multiplayer online mode.

**Key Components:**
- `main.py` - Entry point with mode-based startup logic (polling vs webhook)
- `app/config.py` - Pydantic Settings for environment-based configuration
- `app/game/logic.py` - Core game engine with minimax AI implementation
- `app/handlers/game_handlers.py` - Aiogram Router with command/callback handlers
- `app/keyboards/game_keyboards.py` - InlineKeyboardMarkup builders

**Critical Design Decision:** Game state is stored in-memory (`games: dict[int, TicTacToeGame]` in handlers) per user ID. This is intentional for the current single-player vs AI mode, but when implementing multiplayer, this must be replaced with persistent storage (Redis/PostgreSQL).

## Package Management - UV

**Always use UV, never pip:**
```bash
uv sync              # Install/update all dependencies
uv add package-name  # Add new dependency
uv run python main.py # Run with project environment
```

**Critical:** `pyproject.toml` requires `[tool.hatch.build.targets.wheel]` with `packages = ["app"]` because the package name (`tic-tac-toe-tg`) doesn't match directory name (`app`). Don't remove this.

## Configuration System

Uses **Pydantic Settings** with `.env` file (never commit `.env`, only `.env.example`):

```python
from app.config import settings, BotMode

# Settings auto-loads from .env
settings.bot_token      # Required
settings.bot_mode       # BotMode.POLLING or BotMode.WEBHOOK
settings.webhook_url    # Only for production
```

**Deployment modes:**
- **Local dev:** `BOT_MODE=polling` (uses long polling, no external URL needed)
- **Production:** `BOT_MODE=webhook` (uses aiohttp web server on port 8080)

The bot automatically configures itself based on `bot_mode` in `main.py:main()`.

## Aiogram 3.x Patterns

**Handler registration:**
```python
router = Router()  # Create per-module router

@router.message(Command("start"))  # Command filter
async def handler(message: Message) -> None: ...

@router.callback_query(F.data == "action")  # Magic filter
async def handler(callback: CallbackQuery) -> None: ...

# In main.py
dp.include_router(game_handlers.router)
```

**Callback data format:** Use format `"action_param1_param2"` (e.g., `"move_0_2"` for row 0, col 2). Parse with `callback.data.split("_")`.

**Inline keyboards:** Always return new `InlineKeyboardMarkup` on state change. Aiogram 3 uses `inline_keyboard` parameter (not `keyboard`):
```python
InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
```

## Game Logic Architecture

`TicTacToeGame` is a **dataclass** with:
- `board: list[list[str]]` - 3x3 grid of emoji strings
- `current_player: str` - Emoji string (❌ or ⭕)
- `game_state: str` - GameState enum value

**AI Implementation:** Uses minimax algorithm in `make_ai_move()`. The AI is **intentionally unbeatable** - it evaluates all possible moves to find optimal play. Returns tuple `(row, col)` of AI move or `None` if game over.

**Game flow in handlers:**
1. Player clicks cell → `callback_make_move()` validates and applies move
2. If game continues, immediately call `game.make_ai_move()` (synchronous AI)
3. Update message with new board state using `callback.message.edit_text()`

## Type System

**Strict typing is enforced:**
- All functions have return type hints (`-> None`, `-> bool`, etc.)
- Use `from typing import Optional` for nullable types
- Enums inherit from `str, Enum` for JSON serialization: `class Player(str, Enum)`
- Modern syntax: `dict[int, TicTacToeGame]` not `Dict[int, TicTacToeGame]`

## Testing & Development

**No test suite currently exists.** When adding tests:
- Use pytest with aiogram's testing utilities
- Mock the `games` dictionary for handler tests
- Test minimax algorithm with known board states

**Running bot:**
```bash
uv run python main.py  # Requires BOT_TOKEN in .env
```

**Linting:**
```bash
uv run ruff check app/ main.py
uv run mypy app/ main.py
```

## Future Scalability Considerations

**For multiplayer mode implementation:**
1. Replace in-memory `games` dict with Redis/PostgreSQL
2. Add game session IDs separate from user IDs
3. Implement matchmaking queue in handlers
4. Add game state sync for concurrent moves
5. Consider adding `app/database/` module for persistence layer

**Current architecture supports this** - handlers are already separated, game logic is stateless (operates on passed game instance), and config system can easily add database URLs.

## Common Pitfalls

- **Don't use `asyncio.sleep()` in handlers** - aiogram has built-in rate limiting
- **Always await `callback.answer()`** after processing callbacks (shows loading state resolved)
- **Emoji strings in enums** require UTF-8 encoding - already configured in `pydantic_settings`
- **Webhook mode requires HTTPS** - use ngrok/cloudflare tunnel for local testing
- **Game state isn't persisted** - bot restart clears all active games (by design for now)

## Serena MCP automation guidance
- Use Serena project name `tic-tac-toe_tg`.
- Use Serena for symbol-level edits (find/replace function bodies, insert helpers).
- Use Serena-run snippets to init schema and run quick DB checks.

# Use Serena MCP
- If Serena MCP is available, use its tools as the primary way to search and edit code (symbol-level: find symbols/references, targeted insertions/replacements) instead of reading entire files.
- If Serena is not activated or the project is not indexed — ask me to activate the project `tic-tac-toe_tg` and start indexing, then continue.
- Before major changes: briefly outline a plan, ask for confirmation, and show a minimal unified diff patch in the response.
- After edits: check build/tests and suggest next steps.
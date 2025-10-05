"""Main bot application"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

from app.config import settings, BotMode
from app.handlers import game_handlers


# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Actions on bot startup"""
    if settings.bot_mode == BotMode.WEBHOOK:
        webhook_url = f"{settings.webhook_url}{settings.webhook_path}"
        await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Polling mode enabled")


async def on_shutdown(bot: Bot) -> None:
    """Actions on bot shutdown"""
    if settings.bot_mode == BotMode.WEBHOOK:
        await bot.delete_webhook()
    logger.info("Bot stopped")


async def run_polling(bot: Bot, dp: Dispatcher) -> None:
    """Run bot in polling mode (for local development)"""
    logger.info("Starting bot in polling mode...")
    await on_startup(bot)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await on_shutdown(bot)


async def run_webhook(bot: Bot, dp: Dispatcher) -> None:
    """Run bot in webhook mode (for production)"""
    logger.info("Starting bot in webhook mode...")
    await on_startup(bot)

    # Setup aiohttp web app
    app = web.Application()

    # Create webhook handler
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler

    webhook_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_handler.register(app, path=settings.webhook_path)

    # Setup runner
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host=settings.webapp_host, port=settings.webapp_port)

    try:
        await site.start()
        logger.info(
            f"Webhook server started on {settings.webapp_host}:{settings.webapp_port}"
        )
        # Keep the server running
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()
        await on_shutdown(bot)


async def main() -> None:
    """Main function to run the bot"""
    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # Register handlers
    dp.include_router(game_handlers.router)

    # Run bot based on mode
    if settings.bot_mode == BotMode.WEBHOOK:
        await run_webhook(bot, dp)
    else:
        await run_polling(bot, dp)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

import asyncio
import sys

from loguru import logger

from telegram.core.loader import bot, dp
from telegram.handlers import get_handlers_router
# from telegram.keyboards.default_commands import remove_default_commands, set_default_commands

from telegram.core.config import get_settings


if sys.platform != "win32":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

settings = get_settings()

async def on_startup() -> None:
    logger.info("bot starting...")

    dp.include_router(get_handlers_router())
    #
    # await set_default_commands(bot)

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This is not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("bot started")


async def on_shutdown() -> None:
    logger.info("bot stopping...")

    # await remove_default_commands(bot)

    await bot.session.close()

    logger.info("bot stopped")


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

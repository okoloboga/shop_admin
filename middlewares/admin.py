import logging

from typing import Any, Awaitable, Callable, Dict
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


class AdminMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:

        admins = data.get('admins')

        user: User = data.get('event_from_user').id

        if user and user in admins:
            return await handler(event, data)
        else:
            logger.warning(f'User {user} is not Admin')
            return

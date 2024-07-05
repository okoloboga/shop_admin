import logging

from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input.text import ManagedTextInput

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from fluentogram import TranslatorRunner

from states import ConfirmOrderSG

router_start = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Selecting order for confirmation
async def select_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
        order: str
):
    logger.info(f'User {callback.from_user.id} selected order {order}')
    dialog_manager.current_context().dialog_data['order'] = order
    
    await dialog_manager.switch_to(ConfirmOrderSG.selected_order)
    

# Filled wrong order
async def wrong_order(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.warning(f'User {callback.from_user.id} fills wrong order')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.order())


# Accepting order
async def accept_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):  
    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} accepting order {order}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    await callback.answer(text=i18n.accepting.order(
                                    order=order
                                )
                          )
    await dialog_manager.switch_to(ConfirmOrderSG.accept_order)


# Declining order
async def decline_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):  
    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} declining order {order}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    await callback.answer(text=i18n.declining.order(
                                    order=order
                                )
                          )
    await dialog_manager.switch_to(ConfirmOrderSG.decline_order)
    

# Confirming order accept
async def confirm_accept_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    user_id = callback.from_user.id
    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} confirm orders {order} accept')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)


# Confirming order decline


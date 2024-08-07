import logging

from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input.text import ManagedTextInput

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from fluentogram import TranslatorRunner

from services.services import change_order_status, decline_order_process
from states import ConfirmOrderSG

router_start = Router()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)


# Status New selected
async def new_orders(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
):
    logger.info(f'User {callback.from_user.id} watching for NEW order')
    dialog_manager.current_context().dialog_data['status'] = 'new'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)
 
 
# Status Accepted selected
async def accepted_orders(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
):
    logger.info(f'User {callback.from_user.id} watching for ACCEPTED orders')
    dialog_manager.current_context().dialog_data['status'] = 'accepted'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order) 


# Status Declined selected
async def declined_orders(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
):
    logger.info(f'User {callback.from_user.id} watching for DECLINED orders')
    dialog_manager.current_context().dialog_data['status'] = 'declined'
    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)
    

# Selecting order from list with saved status
async def select_order(
    callback: CallbackQuery,
    db_engine: AsyncEngine,
    dialog_manager: DialogManager,
    order: str
):  
    status = dialog_manager.current_context().dialog_data['status']
    dialog_manager.current_context().dialog_manager['order'] = order
    logger.info(f'User {callback.from_user.id} select #{order} of {status}')
    
    if status == 'new':
        await dialog_manager.switch_to(ConfirmOrderSG.new_order)
        
    elif status == 'accepted':
        await dialog_manager.switch_to(ConfirmOrderSG.accepted_order)
        
    elif status == 'declined':
        await dialog_manager.switch_to(ConfirmOrderSG.declined_order)
        
    elif status == 'completed':
        await dialog_manager.switch_to(ConfirmOrderSG.completed_order)
    
    

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
    status = dialog_manager.current_context().dialog_data['status']
    logger.info(f'User {callback.from_user.id} confirm orders #{order} accept')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    accepted_order = change_order_status(i18n=i18n,
                                         db_engine=db_engine,
                                         user_id=user_id,
                                         order=order,  
                                         status=status     
    )
    
    await callback.answer(text=i18n.accept.costumers.username(
                                    username=accepted_order)
                          )    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)


# Confirming order decline
async def confirm_decline_order(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager,
        reason: str
):
    user_id = callback.from_user.id
    order = dialog_manager.current_context().dialog_data['order']
    logger.info(f'User {callback.from_user.id} confirm orders #{order} decline\
        reason:\n{reason}')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    declined_order = decline_order_process(i18n=i18n,
                                           db_engine=db_engine,
                                           user_id=user_id,
                                           order=order,
                                           reason=reason
    )
    
    await callback.answer(text=i18n.decline.costumers.username(
                                    username=declined_order)
                          )
    await dialog_manager.switch_to(ConfirmOrderSG.select_order) 
    

# Filled wrong reason 
async def wrong_reason(
        callback: CallbackQuery,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text_input: TextInput
):
    logger.info(f'User {callback.from_user.id} fills wrong reason')

    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.wrong.reason())
    
    
# Complete order that in process
async def complete_order(
        callback: CallbackQuery,
        db_engine: AsyncEngine,
        dialog_manager: DialogManager
):
    user_id = callback.from_user.id
    order = dialog_manager.current_context().dialog_data['order']
    status = dialog_manager.current_context().dialog_data['status']
    logger.info(f'User {callback.from_user.id} confirm orders #{order} accept')
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    
    completed_order = change_order_status(i18n=i18n,
                                          db_engine=db_engine,
                                          user_id=user_id,
                                          order=order,
                                          status=status       
    )
    
    await callback.answer(text=i18n.complete.costumers.username(
                                    username=completed_order)
                          )    
    await dialog_manager.switch_to(ConfirmOrderSG.select_order)


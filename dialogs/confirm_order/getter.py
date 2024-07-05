import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database.tables import users, orders
from services.services import (get_item_metadata, delete_item, 
                               change_item, get_order_data)


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Show orders from costumers
async def select_order_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')

    user_id = user_dict['user_id']
    orders_list: list  # Empty tuple for orders

    logger.info(f'User {user_id} in confirm order menu')

    # Getting list of orders
    orders_list_statement = (select(column("index"), column("date_and_time"), 
                        column("name"), column("count"))
                 .select_from(orders)
    )
    async with db_engine.connect() as conn:
        orders_raw = await conn.execute(orders_list_statement)
        for row in orders_raw:
            orders_list.append(list(row))
            logger.info(f'Order with index {list(row)[0]} is executed {list(row)[1:]}')

    return {'orders_list': i18n.orders.list(),
            'orders': tuple(orders_list),
            'button_back': i18n.button.back()}
    
    
# Selected one of orders... Order information
async def selected_order_getter(
        dialog_manager: DialogManager,
        db_engine: AsyncEngine,
        i18n: TranslatorRunner,
        event_from_user: User,
        **kwargs
):  
    user_dict = dialog_manager.start_data
    if type(user_dict) is None:
        logger.error(f'User dict from DialogManager is {user_dict}')
    else:
        logger.info(f'User dict from DialogManager is {user_dict}')

    user_id = user_dict['user_id']   
    order = dialog_manager.current_context().dialog_data['order']
    
    selected_order = get_order_data(db_engine, order)
            
    return {"button_decline": i18n.decline.order(),
            "button_confirm": i18n.button.confirm(),
            "button_accept_order": i18n.accept.order(),
            "button_decline_order": i18n.decline.order(),
            "button_back": i18n.button.back(),
            "selected_order": i18n.selected.order(),
            "accept-order": i18n.accept.order(),
            "decline-order": i18n.decline.order(),
            "order-data": i18n.order.data(
                index=selected_order[0],
                user_id=selected_order[1],
                username=selected_order[2],
                delivery_address=selected_order[3],
                date_and_time=selected_order[4],
                item_index=selected_order[5],
                category=selected_order[6],
                name=selected_order[7],
                count=selected_order[8],
                income=selected_order[9],
                pure_income=selected_order[10]
                )
            }
    
    
        
        
    
        
    



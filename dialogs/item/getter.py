import logging

from aiogram_dialog import DialogManager
from aiogram.types import User
from fluentogram import TranslatorRunner

from sqlalchemy import select, column, func
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from services import get_item_metadata
from database import users, catalogue

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Processing switch to previous page
async def start_previous_getter(
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

    logger.info(f'User {user_id} pressed PREVIOUS button')

    page: int  # Current page of user from database
    new_page: int  # Users page after updating
    catalogue_len: int  # Number of items in catalogue

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    # Get number of items in catalogue
    count = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        count_raw = await conn.execute(count)
        for row in count_raw:
            catalogue_len = row[0]
            logger.info(f'{catalogue_len} items total in Catalogue')
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')

    if page == 0:
        # New page value, if current page is 0
        new_page = catalogue_len - 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    else:
        # New page value, if current page bigger than 0
        new_page = page - 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    # Getting data of NFT item from new Users page
    item = await get_item_metadata(int(new_page), db_engine)

    return {"button_back": i18n.button.back(),
            "button_next": i18n.button.next(),
            "button_edit_row": i18n.button.edit.row(),
            "button_catalogue": i18n.button.catalogue(),
            "item_show": i18n.item.show(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            )
            }


# Processing switch ot next page
async def start_next_getter(
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

    logger.info(f'User {user_id} presser NEXT button')

    page: int  # Current page of user from database
    new_page: int  # Users page after updating
    catalogue_len: int  # Number of items in catalogue

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == user_id)
    )

    # Get number of items in catalogue
    count = (
        select(func.count())
        .select_from(catalogue)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        count_raw = await conn.execute(count)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {user_id}, page is {page}')
        for row in count_raw:
            catalogue_len = row[0]
            logger.info(f'{catalogue_len} items total in Catalogue')

    if page == catalogue_len - 1:
        # New page value, if current page is equal number of items in catalogue
        new_page = 0
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    else:
        # New page value, if current page is less than number of items in catalogue
        new_page = page + 1
        update_page = (users.update()
                       .values(page=new_page)
                       .where(users.c.telegram_id == user_id)
                       )
        # Commit to database
        async with db_engine.connect() as conn:
            await conn.execute(update_page)
            await conn.commit()
            logger.info(f'Users {user_id} page is updated to {new_page}')

    # Getting data of NFT item from new Users page
    item = await get_item_metadata(int(new_page), db_engine)

    return {"button_back": i18n.button.back(),
            "button_next": i18n.button.next(),
            "button_edit_row": i18n.button.edit.row(),
            "button_catalogue": i18n.button.catalogue(),
            "item_show": i18n.item.show(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            )
            }


# Show selected item from catalogue
async def show_item_getter(
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
    item_id = user_dict['item_id']

    logger.info(f'User {user_id} select item №{item_id} from catalogue')

    # Rewrite User page to ITEM_ID
    update_page = (users.update()
                   .values(page=item_id)
                   .where(users.c.telegram_id == user_id)
                   )
    # Commit to database
    async with db_engine.connect() as conn:
        await conn.execute(update_page)
        await conn.commit()
        logger.info(f'Users {user_id} page is updated to {item_id}')

    # Getting data of NFT item from new Users page
    item = await get_item_metadata(int(item_id), db_engine)

    return {"button_back": i18n.button.back(),
            "button_next": i18n.button.next(),
            "button_edit_row": i18n.button.edit.row(),
            "button_catalogue": i18n.button.catalogue(),
            "item_show": i18n.item.show(
                category=item['category'],
                name=item['name'],
                description=item['description'],
                image=item['image'],
                sell_price=item['sell_price'],
                self_price=item['self_price'],
                count=item['count']
            )
            }

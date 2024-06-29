import logging
import validators

from datetime import datetime
from aiogram_dialog import DialogManager

from sqlalchemy import insert, delete, select, column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from database import users, catalogue, income, edited
from .ton_services import wallet_deploy

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s')


# Get item from database
async def get_item_metadata(number: int,
                            db_engine: AsyncEngine
                            ) -> dict:
    logger.info(f'get_item_metadata({number})')
    result: list  # Main data of item

    # Getting item by index
    statement = (
        select(column("category"), column("name"), column("description"),
               column("image"), column("sell_price"), column("self_price"),
               column("count"))
        .select_from(catalogue)
        .where(catalogue.c.index == number)
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            result = list(row)  # row is tuple!
            logger.info(f'Item with index {number} is executed: {result}')

    # To Dict
    item = {
            "category": result[0],
            "name": result[1],
            "description": result[2],
            "image": result[3],
            "sell_price": result[4],
            "self_price": result[5],
            "count": result[6]
    }

    return item


# Getting users with non-user status
async def get_admins_list(db_engine: AsyncEngine) -> list:
    logger.info(f'Getting list of admins...')
    admins = []

    # Getting ID's by status
    statement = (
        select(column("telegram_id"))
        .select_from(users)
        .where(users.c.status != 'user')
    )
    async with db_engine.connect() as conn:
        result_raw = await conn.execute(statement)
        for row in result_raw:
            admins.append(row[0])
            logger.info(f'{row[0]} executed as Admin')

    return admins


# Checking for URL
def check_url(url: str) -> str:
    if validators.url(url):
        return url
    raise ValueError


# Checking Sell price, Self price and count
def check_price_count(text: str) -> str:
    text_list = text.split()
    if len(text_list) == 3:
        for i in text_list:
            if not i.isdigit():
                raise ValueError
        else:
            return text
    raise ValueError


# Writing new Item to database
async def new_item(
        db_engine: AsyncEngine,
        admin_id: int,
        new_item_data: dict
):
    logger.info(f'new_item({new_item_data['name']})')

    len_catalogue: int  # Number of items in Catalogue table
    len_income: int  # Number of items in Income table

    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting length of Catalogue and Income tables
    len_catalogue_statement = (
        select(func.count())
        .select_from(catalogue)
    )
    len_income_statement = (
        select(func.count())
        .select_from(income)
    )

    async with db_engine.connect() as conn:
        raw_catalogue_len = await conn.execute(len_catalogue_statement)
        raw_income_len = await conn.execute(len_income_statement)
        for row in raw_catalogue_len:
            len_catalogue = int(row[0])
            logger.info(f'Catalogue table length is {len_catalogue}')
        for row in raw_income_len:
            len_income = int(row[0])
            logger.info(f'Income table length is {len_income}')

    # Writing statements for Catalogue and Income tables
    catalogue_statement = insert(catalogue).values(
        index=len_catalogue,
        category=new_item_data['category'],
        name=new_item_data['name'],
        description=new_item_data['description'],
        image=new_item_data['image'],
        self_price=new_item_data['self_price'],
        sell_price=new_item_data['sell_price'],
        count=new_item_data['count'],
    )

    income_statement = insert(income).values(
        index=len_income,
        admin_id=admin_id,
        date_and_time=date_and_time,
        item_index=len_catalogue,
        category=new_item_data['category'],
        name=new_item_data['name'],
        count=new_item_data['count'],
        income_sellprice=int(new_item_data['count']) * int(new_item_data['sell_price']),
        income_selfprice=int(new_item_data['count']) * int(new_item_data['self_price']),
    )

    async with db_engine.connect() as conn:
        await conn.execute(catalogue_statement)
        await conn.execute(income_statement)
        await conn.commit()
        logger.info('New item in Catalogue and Income are commited')


# Deleting item from database
async def delete_item(
        db_engine: AsyncEngine,
        admin_id: int,
):
    logger.info(f'delete_item({admin_id})')
    page: int  # Current page of user from database

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == admin_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {admin_id}, page is {page}')

    # Delete current item
    delete_item_statement = (
        delete(catalogue)
        .where(catalogue.c.index == page)
    )

    # Commit to database
    async with db_engine.connect() as conn:
        await conn.execute(delete_item_statement)
        await conn.commit()
        logger.info(f'User {admin_id} deleted item #{page}')


# Validate changes entered by Admin
def check_changes(changes: str) -> dict:
    changes_types = {
                     'category': str,
                     'name': str,
                     'description': str,
                     'image': str,
                     'sell_price': int,
                     'self_price': int,
                     'count': int
    }

    if changes[0] == '#':

        # drop #
        changes_raw = changes[1:].split()

        # is correct type of change
        if changes_raw[0] in changes_types:

            # unite changes description, like {'description': 'very taste banana'}
            changes_united = {changes_raw[0]: ' '.join(changes_raw[1:])}

            # check for data type of changes
            if changes_types[changes_united[0]] is type(changes_united[1]):
                if (((changes_united[0] == 'image')
                        and validators.url(changes_united[1]))
                        or changes_united[0] != 'image'):
                    return changes_united
                raise ValueError
            raise ValueError
        raise ValueError
    raise ValueError


# Writing changes of item in database
async def change_item(
        db_engine: AsyncEngine,
        admin_id: int,
        new_data: dict
):
    logger.info(f'change_item({admin_id}, {new_data})')
    len_edited: int  # Number of items in Edited table
    page: int  # Current page of user from database

    # Get current users page
    user_page = (
        select(column("page"))
        .select_from(users)
        .where(users.c.telegram_id == admin_id)
    )

    async with db_engine.connect() as conn:
        page_raw = await conn.execute(user_page)
        for row in page_raw:
            page = row[0]
            logger.info(f'Statement PAGE: {row[0]} executed of user {admin_id}, page is {page}')

    # Getting current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    date_and_time = now.strftime("%d/%m/%Y %H:%M:%S")

    # Getting length of Edited tables
    len_edited_statement = (
        select(func.count())
        .select_from(edited)
    )

    async with db_engine.connect() as conn:
        raw_edited_len = await conn.execute(len_edited_statement)
        for row in raw_edited_len:
            len_edited = int(row[0])
            logger.info(f'Catalogue table length is {len_edited}')

    # Getting item metadata
    item = await get_item_metadata(
        int(page),
        db_engine
    )

    # Insert new row to Edited table
    edited_statement = insert(edited).values(
        index=len_edited,
        admin_id=admin_id,
        date_and_time=date_and_time,
        item_index=page,
        category=item['category'],
        name=item['name'],
        commit=' '.join(new_data)
    )

    # Update data in Catalogue table
    update_catalogue = (catalogue.update()
                        .values(**new_data)
                        .where(catalogue.c.index == page)
                        )

    async with db_engine.connect() as conn:
        await conn.execute(update_catalogue)
        await conn.execute(edited_statement)
        await conn.commit()
        logger.info(f'Users {admin_id} page is updated to {page}')




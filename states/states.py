from aiogram.fsm.state import State, StatesGroup


class ItemSG(StatesGroup):
    start = State()
    start_previous = State()
    start_next = State()
    show_item = State()


class CatalogueSG(StatesGroup):
    catalogue = State()


class StartSG(StatesGroup):
    main = State()


class AddRowSG(StatesGroup):
    add_row = State()
    fill_category = State()
    fill_name = State()
    fill_description = State()
    fill_image = State()
    fill_price_count = State()
    confirm = State()
    complete = State()


class EditRowSG(StatesGroup):
    edit_row = State()
    edit = State()
    delete = State()
    delete_confirmed = State()
    changes_confirmed = State()

class ConfirmOrderSG(StatesGroup):
    select_status = State()
    select_order = State()
    new_order = State()
    accept_order = State()
    decline_order = State()
    accepted_order = State()
    declined_order = State()
    completed_order = State()

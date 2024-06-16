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


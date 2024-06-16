from aiogram.types import ContentType

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.kbd import Button, Row

from states import StartSG
from .getter import *
from .handler import *


start_dialog = Dialog(
    Window(
        Format('{start}'),
        Button(Format('{button_add_row}'), id='b_add_row', on_click=add_row),
        Button(Format('{button_catalogue}'), id='catalogue', on_click=switch_to_catalogue),
        getter=start_getter,
        state=StartSG.main
    )
)
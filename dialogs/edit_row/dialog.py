from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from states import EditRowSG

from .getter import *
from .handler import *
from ..start import go_start



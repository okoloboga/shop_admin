from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, List
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.widgets.kbd import Button, Row

from states import ConfirmOrderSG

from .getter import *
from .handler import *
from ..start import go_start
from services.services import check_order


"""Confirming orders"""
comfirm_order = Dialog(
    Window(
        Format('{orders_list}'),
        List(field=Format('<b>#{item[0]}</b> {item[1]} {item[2]} {item[3]}'),
            items='orders'),
                TextInput(
                    id='select_order',
                    type_factory=check_order,
                    on_success=select_order,
                    on_error=wrong_order
            ),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=select_order_getter,
        state=ConfirmOrderSG.select_order
    ),
    Window(
        Format('{selected_order}'),
        Format('{order_data}'),       
        Button(Format('{button_accept_order}'), id='b_accept_order', on_click=accept_order),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        Button(Format('{button_decline_order}'), id='b_decline_order', on_click=decline_order),
        getter=selected_order_getter,
        state=ConfirmOrderSG.selected_order
    ),
    Window(
        Format('{accept_order}'),
        Format('{order_data}'),
        Button(Format('{button_confirm_accept_order}', 
                      id='b_confirm_accept_order', 
                      on_click=confirm_accept_order)),
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=accept_order_getter,
        state=ConfirmOrderSG.accept_order
    ),
    Window(
        Format('{decline_order}'),
        Format('{order_data}'),   
        Button(Format('{button_confirm_decline_order}', 
                      id='b_confirm_decline_order', 
                      on_click=confirm_decline_order)), 
        Button(Format('{button_back}'), id='b_back', on_click=go_start),
        getter=decline_order_getter,
        state=ConfirmOrderSG.decline_order
    )
)
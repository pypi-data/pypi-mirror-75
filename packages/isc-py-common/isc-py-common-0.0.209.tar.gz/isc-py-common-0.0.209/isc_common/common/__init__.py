import os
from typing import Text
from uuid import UUID


def getOrElse(default, value):
    if value:
        return value
    else:
        return default


blue = 'blue'
closed = 'closed'
create = 'create'
deleted = 'deleted'
doing = 'doing'
green = 'green'
made = 'made'
new = 'new'
new_man = 'new_man'
red = 'red'
restarted = 'restarted'
started = 'started'
transferred = 'transferred'
update = 'update'
value_odd = 'value_odd'


def blinkString(text, blink=True, color="black", bold=False) -> Text:
    if blink:
        res = f'<div class="blink"><strong><font color="{color}"</font>{text}</strong></div>'
    else:
        res = f'<div><strong><font color="{color}"</font>{text}</strong></div>'

    if bold == True:
        return f'<b>{res}</b>'
    else:
        return res


def uuid4():
    return str(UUID(bytes=os.urandom(16), version=4)).upper().replace('-', '_')

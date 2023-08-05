from typing import Text


def getOrElse(default, value):
    if value:
        return value
    else:
        return default

blue='blue'
closed='closed'
create='create'
deleted='deleted'
doing='doing'
green='green'
made='made'
new='new'
new_man='new_man'
red='red'
restarted='restarted'
started='started'
transferred='transferred'
update='update'

def blinkString(text, blink=True, color="black", bold=False) -> Text:
    if blink:
        res = f'<div class="blink"><strong><font color="{color}"</font>{text}</strong></div>'
    else:
        res = f'<div><strong><font color="{color}"</font>{text}</strong></div>'

    if bold == True:
        return f'<b>{res}</b>'
    else:
        return res

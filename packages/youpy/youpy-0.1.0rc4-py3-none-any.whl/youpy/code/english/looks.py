# -*- encoding: utf-8 -*-
"""Front-end API functions of the "looks" category.
"""


from youpy.api import get_scene
from youpy.api import send_request
from youpy.api import get_context_sprite_name
from youpy.api import message


def switch_backdrop_to(backdrop):
    # TODO(Nicolas Despres): Add wait keyword argument to mimic the
    #   "switch to <backdrop> and wait" block?
    if not isinstance(backdrop, str):
        raise TypeError("backdrop must be str, not {}"
                        .format(type(backdrop).__name__))
    send_request(message.BackdropSwitchTo(name=backdrop))

def show():
    """Show the current sprite."""
    sprite_name = get_context_sprite_name()
    send_request(message.SpriteOp(name=sprite_name, op="show"))

def hide():
    """Hide the current sprite."""
    sprite_name = get_context_sprite_name()
    send_request(message.SpriteOp(name=sprite_name, op="hide"))

__all__ = (
    "hide",
    "show",
    "switch_backdrop_to",
)

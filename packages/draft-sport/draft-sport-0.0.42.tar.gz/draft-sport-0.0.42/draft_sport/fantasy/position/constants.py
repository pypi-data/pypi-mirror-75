"""
Draft Sport Python
Fantasy Position Constants Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.position.position import Position
from draft_sport.universe.position.constants import CategoryConstants

_FORWARD_CAT = [CategoryConstants.SUPER_RUGBY_FORWARD]
_BACK_CAT = [CategoryConstants.SUPER_RUGBY_BACK]


class PositionConstants:

    SUPER_RUGBY_PROP = Position(1, 'Prop', _FORWARD_CAT)
    SUPER_RUGBY_HOOKER = Position(2, 'Hooker', _FORWARD_CAT)
    SUPER_RUGBY_LOCK = Position(3, 'Lock', _FORWARD_CAT)
    SUPER_RUGBY_BACK_ROW = Position(4, 'Back Row', _FORWARD_CAT)
    SUPER_RUGBY_SCRUMHALF = Position(5, 'Scrumhalf', _BACK_CAT)
    SUPER_RUGBY_FLYHALF = Position(6, 'Flyhalf', _BACK_CAT)
    SUPER_RUGBY_OUTSIDE_BACK = Position(7, 'Outside Back', _BACK_CAT)
    SUPER_RUGBY_CENTRE = Position(8, 'Centre', _BACK_CAT)

    SUPER_RUGBY = (
        SUPER_RUGBY_PROP,
        SUPER_RUGBY_HOOKER,
        SUPER_RUGBY_LOCK,
        SUPER_RUGBY_BACK_ROW,
        SUPER_RUGBY_SCRUMHALF,
        SUPER_RUGBY_FLYHALF,
        SUPER_RUGBY_OUTSIDE_BACK,
        SUPER_RUGBY_CENTRE
    )

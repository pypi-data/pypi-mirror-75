"""
Draft Sport Python
Universe Position Constants Module
author: hugh@blinkybeach.com
"""
from draft_sport.universe.position.category import PositionCategory


class CategoryConstants:

    SUPER_RUGBY_BACK = PositionCategory(1, 'back')
    SUPER_RUGBY_FORWARD = PositionCategory(2, 'forward')

    SUPER_RUGBY = (
        SUPER_RUGBY_FORWARD,
        SUPER_RUGBY_BACK
    )

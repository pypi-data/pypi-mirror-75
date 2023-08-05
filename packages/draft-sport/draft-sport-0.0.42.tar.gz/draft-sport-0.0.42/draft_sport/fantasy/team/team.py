"""
Draft Sport Python
Fantasy Team Class
author: hugh@blinkybeach.com
"""
from nozomi import Immutable


class Team:

    def __init__(
        self,
        name: str
    ) -> None:

        self._name = name

        return

    name = Immutable(lambda s: s._name)
    lowercase_name = Immutable(lambda s: s._name.lower())

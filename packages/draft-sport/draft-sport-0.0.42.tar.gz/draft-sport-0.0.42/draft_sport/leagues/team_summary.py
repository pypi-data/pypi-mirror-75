"""
Draft Sport Python
Team Summary Module
author: hugh@blinkybeach.com
"""
from typing import TypeVar, Type, Any
from nozomi import Decodable, Immutable

T = TypeVar('T', bound='TeamSummary')


class TeamSummary(Decodable):

    def __init__(
        self,
        manager_id: str,
        manager_name: str,
        team_name: str,
        league_id: str
    ) -> None:

        self._manager_id = manager_id
        self._manager_name = manager_name
        self._team_name = team_name
        self._league_id = league_id

        return

    manager_id = Immutable(lambda s: s._manager_id)
    manager_name = Immutable(lambda s: s._manager_name)
    team_name = Immutable(lambda s: s._team_name)
    league_id = Immutable(lambda s: s._league_id)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            manager_id=data['manager_public_id'],
            manager_name=data['manager_name'],
            league_id=data['league_public_id'],
            team_name=data['team_name']
        )

"""
Draft Sport
Pick Module
author: hugh@blinkybeach.com
"""
from draft_sport.fantasy.player.profile import Profile
from nozomi import Decodable, NozomiTime, Immutable
from typing import TypeVar, Type, Any

T = TypeVar('T', bound='Pick')


class Pick(Decodable):

    def __init__(
        self,
        created: NozomiTime,
        manager_id: str,
        profile: Profile,
        league_id: str,
        as_at: NozomiTime
    ) -> None:

        self._created = created
        self._manager_id = manager_id
        self._profile = profile
        self._league_id = league_id
        self._as_at = as_at

        return

    profile = Immutable(lambda s: s._profile)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            created=NozomiTime.decode(data['created']),
            manager_id=data['manager_id'],
            profile=Profile.decode(data['player']),
            league_id=data['league_id'],
            as_at=NozomiTime.decode(data['as_at'])
        )

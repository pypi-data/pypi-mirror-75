import json
from itertools import chain

from ..util import dict_get_value
from ..cached_property import cached_property


def _try_parse_json(data: str) -> dict:
    try:
        return json.loads(data)
    except (TypeError, json.JSONDecodeError) as _:
        return {}


class PubSubData:
    MESSAGE_TYPE = 'MESSAGE'
    REWARD_REDEEMED_TYPE = 'reward-redeemed'

    def __init__(self, raw_data: dict):
        self.raw_data: dict = raw_data

    def is_type(self, type: str):
        return self.raw_data.get('type').lower() == type.lower()

    @cached_property
    def is_pong(self):
        return self.is_type('PONG')

    @cached_property
    def is_channel_points_redeemed(self):
        return self.is_type(self.MESSAGE_TYPE) and self.message_dict.get('type', '').lower() == self.REWARD_REDEEMED_TYPE.lower()

    @cached_property
    def channel_point_redemption_dict(self):
        return self.message_data.get('redemption', {})

    @cached_property
    def topic(self) -> str:
        return dict_get_value(self.raw_data, 'data', 'topic', default='')

    @cached_property
    def message_dict(self):
        return _try_parse_json(dict_get_value(self.raw_data, 'data', 'message', default='{}'))

    @cached_property
    def message_data(self):
        return self.message_dict.get('data', {})

    @cached_property
    def message_type(self) -> str:
        return self.message_data.get('type', '')

    @cached_property
    def moderation_action(self) -> str:
        return self.message_data.get('moderation_action', '')

    @cached_property
    def args(self) -> list:
        return list(chain.from_iterable(arg.split() for arg in self.message_data.get('args', [])))

    @cached_property
    def created_by(self) -> str:
        return self.message_data.get('created_by', '')

    @cached_property
    def created_by_user_id(self) -> str:
        return self.message_data.get('created_by_user_id', '')

    @cached_property
    def msg_id(self) -> str:
        return self.message_data.get('msg_id', '')

    @cached_property
    def target_user_id(self) -> str:
        return self.message_data.get('target_user_id', '')

    @cached_property
    def target_user_login(self) -> str:
        return self.message_data.get('target_user_login', '')

    @cached_property
    def from_automod(self) -> bool:
        return self.message_data.get('from_automod', False)

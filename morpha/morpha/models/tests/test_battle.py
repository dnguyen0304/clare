# -*- coding: utf-8 -*-

import collections

import mock
from nose.tools import assert_equal, assert_is_instance, assert_true

from .. import Battle, PlayerRecord, PokemonRecord, SwitchRecord


class TestBattle(object):

    def __init__(self):
        self.player_1_record = None
        self.pokemon_record = None
        self.switch_record = None
        self.battle = Battle()

    def setup(self):
        self.player_1_record = PlayerRecord(position=1, name='foo')
        self.pokemon_record = PokemonRecord(
            position=self.player_1_record.position,
            pokemon_name='bar')
        self.switch_record = SwitchRecord(
            position=self.player_1_record.position,
            pokemon_name=self.pokemon_record.pokemon_name,
            remaining_hit_points=0,
            total_hit_points=100)

    def test_apply_log_record(self):
        self.mock_record_handlers()

        self.battle.apply_log_record(self.player_1_record)
        self.battle.handle_player_record.assert_called()

    def test_apply_log_record_missing_handler(self):
        self.mock_record_handlers()

        self.battle.apply_log_record('foo')

    def test_pokemon_are_loaded_flag(self):
        self.battle.apply_log_record(PlayerRecord(position=2, name='eggs'))
        self.set_up_switch_record_handlers()

        assert_true(self.battle.pokemon_are_loaded)

    def test_handle_player_record(self):
        self.set_up_player_record_handlers()

        player = self.battle.get_all_players()[0]
        assert_equal(player.name, self.player_1_record.name)

    def test_handle_pokemon_record(self):
        self.set_up_pokemon_record_handlers()

        player = self.battle.get_all_players()[0]
        assert_equal(player.pokemon[0].name, self.pokemon_record.pokemon_name)

    def test_handle_switch_record(self):
        self.set_up_switch_record_handlers()

        player = self.battle.get_all_players()[0]
        assert_equal(player.pokemon[0].total_hit_points,
                     self.switch_record.total_hit_points)

    def test_get_all_players(self):
        self.set_up_player_record_handlers()

        players = self.battle.get_all_players()
        assert_is_instance(players, collections.Iterable)
        assert_equal(players[0].name, self.player_1_record.name)

    def mock_record_handlers(self):
        for attribute in dir(self.battle):
            if attribute.startswith('handle') and attribute.endswith('record'):
                setattr(self.battle, attribute, mock.MagicMock())

    def set_up_player_record_handlers(self):
        self.battle.apply_log_record(self.player_1_record)

    def set_up_pokemon_record_handlers(self):
        self.set_up_player_record_handlers()
        self.battle.apply_log_record(self.pokemon_record)

    def set_up_switch_record_handlers(self):
        self.set_up_pokemon_record_handlers()
        self.battle.apply_log_record(self.switch_record)

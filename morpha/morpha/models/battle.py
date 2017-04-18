# -*- coding: utf-8 -*-

import collections

from . import (MoveRecord,
               Player,
               PlayerRecord,
               Pokemon,
               PokemonRecord,
               SwitchRecord)


class Side(object):

    def __init__(self, position, player):
        self.position = position
        self.player = player

    def __repr__(self):
        repr_ = '{}(position={}, player={})'
        return repr_.format(self.__class__.__name__,
                            self.position,
                            self.player)


class CurrentAction(object):

    def __init__(self,
                 used_by_player,
                 used_by_pokemon,
                 targeted_player,
                 targeted_pokemon):

        self.used_by_player = used_by_player
        self.used_by_pokemon = used_by_pokemon
        self.targeted_player = targeted_player
        self.targeted_pokemon = targeted_pokemon

    def __repr__(self):
        repr_ = ('{}('
                 'used_by_player={}, '
                 'used_by_pokemon={}, '
                 'targeted_player={}, '
                 'targeted_pokemon={})')
        return repr_.format(self.__class__.__name__,
                            self.used_by_player,
                            self.used_by_pokemon,
                            self.targeted_player,
                            self.targeted_pokemon)


class Battle(object):

    _mapping = {
        PlayerRecord: 'handle_player_record',
        PokemonRecord: 'handle_pokemon_record',
        MoveRecord: 'handle_move_record',
        SwitchRecord: 'handle_switch_record'
    }

    def __init__(self):
        self._sides = list()
        self._sides_index = dict()
        self._players = list()
        self._players_index = dict()
        self._pokemon_index = collections.defaultdict(dict)
        self.pokemon_are_loaded = False
        self.current_action = None

    def apply_log_record(self, log_record):
        if len(self._players) == 2 and not isinstance(log_record, PokemonRecord):
            self.pokemon_are_loaded = True
        try:
            handler = getattr(self, self._mapping[type(log_record)])
        except KeyError:
            pass
        else:
            handler(log_record)

    def handle_player_record(self, record):
        player = Player(name=record.name)
        side = Side(position=record.position, player=player)

        self._sides.append(side)
        self._sides_index[record.position] = side
        self._players.append(player)
        self._players_index[record.position] = player

    def handle_pokemon_record(self, record):
        pokemon = Pokemon(name=record.pokemon_name)
        player = self._players_index[record.position]
        player.pokemon.append(pokemon)

        self._pokemon_index[record.position][pokemon.name] = pokemon

    def handle_move_record(self, record):
        self.current_action = CurrentAction(
            used_by_player=self._players_index[record.used_by_position],
            used_by_pokemon=self._pokemon_index[record.used_by_position][record.used_by_pokemon_name],
            targeted_player=self._players_index[record.targeted_position],
            targeted_pokemon=self._pokemon_index[record.targeted_position][record.targeted_pokemon_name])

    def handle_switch_record(self, record):
        player = self._players_index[record.position]
        for pokemon in player.pokemon:
            if pokemon.name == record.pokemon_name:
                pokemon.total_hit_points = record.total_hit_points
                break

    def get_all_players(self):
        return self._players

    def __repr__(self):
        repr_ = '{}()'
        return repr_.format(self.__class__.__name__)

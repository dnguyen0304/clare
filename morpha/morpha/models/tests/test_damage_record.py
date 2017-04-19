# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import DamageRecord


class TestDamageRecord(object):

    def test_from_message(self):
        message = '|-damage|p1a: eggs|10\/100'
        record = DamageRecord.from_message(message)
        assert_equal(record.remaining_hit_points, 10)

    def test_from_message_faint_status_condition(self):
        message = '|-damage|p1a: eggs|0 fnt'
        record = DamageRecord.from_message(message)
        assert_equal(record.remaining_hit_points, 0)

    def test_from_message_indirect_damage(self):
        message = '|-damage|p1a: eggs|10\/100|[from] Stealth Rock'
        record = DamageRecord.from_message(message)
        assert_equal(record.remaining_hit_points, 10)

    @raises(ValueError)
    def test_from_message_incorrect_format(self):
        message = '|foo'
        DamageRecord.from_message(message)

# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import stop_strategies
from ..attempt import Attempt


def test_after_attempt_greater_than_threshold_should_stop():

    maximum_attempt = 1
    stop_strategy = stop_strategies.AfterAttempt(
        maximum_attempt=maximum_attempt)
    attempt = Attempt(number=maximum_attempt + 1,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_equal_to_threshold_should_not_stop():

    maximum_attempt = 1
    stop_strategy = stop_strategies.AfterAttempt(
        maximum_attempt=maximum_attempt)
    attempt = Attempt(number=maximum_attempt,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_less_than_threshold_should_not_stop():

    maximum_attempt = 1
    stop_strategy = stop_strategies.AfterAttempt(
        maximum_attempt=maximum_attempt)
    attempt = Attempt(number=maximum_attempt - 1,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_stop(attempt=attempt))


def test_after_duration_should_stop_greater_than_maximum_duration():

    maximum_duration = 1
    stop_strategy = stop_strategies.AfterDuration(
        maximum_duration=maximum_duration,
        _get_now_in_seconds=lambda: maximum_duration + 1)
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=0)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_duration_should_stop_equal_to_maximum_duration():

    maximum_duration = 1
    stop_strategy = stop_strategies.AfterDuration(
        maximum_duration=maximum_duration,
        _get_now_in_seconds=lambda: maximum_duration)
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=0)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_duration_should_not_stop():

    maximum_duration = 1
    stop_strategy = stop_strategies.AfterDuration(
        maximum_duration=maximum_duration,
        _get_now_in_seconds=lambda: maximum_duration - 1)
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=0)
    assert_false(stop_strategy.should_stop(attempt=attempt))


def test_after_never_should_not_stop():

    stop_strategy = stop_strategies.AfterNever()
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_stop(attempt=attempt))

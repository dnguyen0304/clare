# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true, raises

from .. import stop_strategies
from ..attempt import Attempt


def test_after_attempt_should_stop_greater_than_maximum_attempt():

    maximum_attempt = 1
    stop_strategy = stop_strategies.AfterAttempt(
        maximum_attempt=maximum_attempt)
    attempt = Attempt(number=maximum_attempt + 1,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_should_stop_equal_to_maximum_attempt():

    maximum_attempt = 1
    stop_strategy = stop_strategies.AfterAttempt(
        maximum_attempt=maximum_attempt)
    attempt = Attempt(number=maximum_attempt,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_attempt_should_not_stop():

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


def test_after_result_should_continue():
    stop_strategy = stop_strategies.AfterResult(predicate=lambda x: x == 'foo')
    attempt = Attempt(number=None,
                      was_successful=None,
                      result='foo',
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_continue(attempt=attempt))


def test_after_result_should_not_continue():
    stop_strategy = stop_strategies.AfterResult(predicate=lambda x: x == 'foo')
    attempt = Attempt(number=None,
                      was_successful=None,
                      result='bar',
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_continue(attempt=attempt))


@raises(TypeError)
def test_after_result_predicate_accepts_one_argument():
    stop_strategy = stop_strategies.AfterResult(predicate=lambda: None)
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    stop_strategy.should_continue(attempt=attempt)


def test_after_success_should_stop():
    stop_strategy = stop_strategies.AfterSuccess()
    attempt = Attempt(number=None,
                      was_successful=True,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(stop_strategy.should_stop(attempt=attempt))


def test_after_success_should_not_stop():
    stop_strategy = stop_strategies.AfterSuccess()
    attempt = Attempt(number=None,
                      was_successful=False,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(stop_strategy.should_stop(attempt=attempt))


def test_should_continue():

    continue_strategy = stop_strategies.AfterNever()
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(continue_strategy.should_continue(attempt=attempt))

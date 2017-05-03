# -*- coding: utf-8 -*-

import time

from . import Attempt


class RetryPolicy(object):

    def __init__(self,
                 stop_strategy,
                 wait_strategy,
                 handled_exceptions=tuple()):

        """
        Parameters
        ----------
        stop_strategy : IStopStrategy
        wait_strategy : IWaitStrategy
        handled_exceptions : collections.Iterable
            Defaults to an empty tuple.
        """

        self._stop_strategy = stop_strategy
        self._wait_strategy = wait_strategy
        self._handled_exceptions = handled_exceptions
        self._attempt = Attempt(number=0,
                                was_successful=None,
                                result=None,
                                exception=None,
                                first_attempt_start_time=time.time())

    def execute(self, callable, _sleep=None):

        """
        Parameters
        ----------
        callable : collections.Callable
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        _sleep = time.sleep if _sleep is None else _sleep

        while True:
            attempt_number = self._attempt.number + 1
            was_successful = False
            result = None
            exception = None

            if (self._attempt.was_successful or
                self._stop_strategy.should_stop(attempt=self._attempt)):
                    break
            try:
                result = callable()
            except self._handled_exceptions as e:
                exception = e
            else:
                was_successful = True

            self._attempt = Attempt(
                number=attempt_number,
                was_successful=was_successful,
                result=result,
                exception=exception,
                first_attempt_start_time=self._attempt.first_attempt_start_time)

            _sleep(self._wait_strategy.compute_wait_time(attempt=self._attempt))

        if self._attempt.was_successful:
            return self._attempt.result

    def __repr__(self):
        repr_ = '{}(stop_strategy={}, wait_strategy={}, handled_exceptions={})'
        return repr_.format(self.__class__.__name__,
                            self._stop_strategy,
                            self._wait_strategy,
                            self._handled_exceptions)

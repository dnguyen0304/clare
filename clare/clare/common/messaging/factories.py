# -*- coding: utf-8 -*-

import datetime

from . import records


class RecordFactory(object):

    def __init__(self, time_zone):

        """
        Parameters
        ----------
        time_zone : datetime.tzinfo
        """

        self._time_zone = time_zone

    def create(self, value=None):

        """
        Parameters
        ----------
        value : typing.Any
        """

        timestamp = datetime.datetime.utcnow().replace(tzinfo=self._time_zone)
        record = records.Record(timestamp=timestamp, value=value)
        return record

    def __repr__(self):
        repr_ = '{}(time_zone={})'
        return repr_.format(self.__class__.__name__, self._time_zone)
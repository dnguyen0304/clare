# -*- coding: utf-8 -*-

from .. import exceptions


class FetchTimeout(exceptions.Timeout):
    pass


class ReceiveTimeout(exceptions.Timeout):
    pass

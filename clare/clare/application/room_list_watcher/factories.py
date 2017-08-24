# -*- coding: utf-8 -*-

import collections
import logging
import sys

from . import adapters
from . import filters
from . import flush_strategies
from . import marshallers
from . import producers
from . import senders
from . import sources
from .automation import factories
from clare.common import messaging
from clare.common import utilities


class Producer(object):

    def __init__(self, infrastructure, properties):

        """
        Parameters
        ----------
        infrastructure : clare.infrastructure.infrastructures.RoomListWatcher
        properties : collections.Mapping
        """

        self._factory = factories.Scraper(properties=properties['scraper'])
        self._infrastructure = infrastructure
        self._properties = properties

    def create(self):
        # Construct the producer.
        dependencies = self.create_dependencies()

        producer = messaging.producer.producers.Producer(
            source=dependencies['source'],
            sender=dependencies['sender'],
            filters=dependencies['filters'])

        # Include orchestration.
        logger = logging.getLogger(name=self._properties['logger']['name'])
        producer = producers.OrchestratingProducer(producer=producer,
                                                   logger=logger)

        return producer

    def create_dependencies(self):

        """
        Returns
        -------
        dict
        """

        dependencies = dict()

        # Construct the source.
        scraper = self._factory.create()
        message_factory = messaging.factories.Message()
        marshaller = marshallers.SeleniumWebElementToMessage(
            message_factory=message_factory)
        source = adapters.ScraperToBufferingSource(
            scraper=scraper,
            url=self._properties['scraper']['url'],
            marshall_strategy=marshaller)
        dependencies['source'] = source

        # Construct the sender.
        sender = senders.Sender(queue=self._infrastructure.produce_to_queue)

        # Include logging.
        logger = logging.getLogger(
            name=self._properties['sender']['logger']['name'])
        sender = senders.Logging(sender=sender, logger=logger)
        dependencies['sender'] = sender

        # Construct the filters.
        dependencies['filters'] = list()

        # Construct the no duplicate filter.
        countdown_timer = utilities.timers.CountdownTimer(
            duration=self._properties['filter']['flush_strategy']['duration'])
        after_duration = flush_strategies.AfterDuration(
            countdown_timer=countdown_timer)
        no_duplicate = filters.NoDuplicateBody(flush_strategy=after_duration)
        dependencies['filters'].append(no_duplicate)

        return dependencies

    def __repr__(self):
        repr_ = '{}(infrastructure={}, properties={})'
        return repr_.format(self.__class__.__name__,
                            self._infrastructure,
                            self._properties)


class CommandLineArgumentsWatcher(Producer):

    def create_dependencies(self):
        dependencies = super(CommandLineArgumentsWatcher, self).create_dependencies()

        # Construct the deque source.
        deque = collections.deque(sys.argv[1:])
        message_factory = messaging.factories.Message()
        source = sources.Deque(deque=deque, message_factory=message_factory)
        dependencies['source'] = source

        return dependencies

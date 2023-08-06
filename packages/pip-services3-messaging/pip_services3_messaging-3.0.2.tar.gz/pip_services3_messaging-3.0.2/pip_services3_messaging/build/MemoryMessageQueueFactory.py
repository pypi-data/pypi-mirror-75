# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.build.MemoryMessageQueueFactory
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    MemoryMessageQueueFactory implementation

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory
from ..queues.MemoryMessageQueue import MemoryMessageQueue

_Descriptor = Descriptor("pip-services-net", "factory", "message-queue", "memory", "1.0")
MemoryQueueDescriptor = Descriptor("pip-services-net", "message-queue", "memory", "*", "*")

class MemoryMessageQueueFactory(Factory):
    """
    Creates [[MemoryMessageQueue]] components by their descriptors.
    Name of created message queue is taken from its descriptor.
    """
    def __init__(self):
        """
        Create a new instance of the factory.
        """
        super(MemoryMessageQueueFactory, self).__init__()
        def register(locator, factory):
            descriptor = locator
            return MemoryMessageQueue(descriptor.get_name())
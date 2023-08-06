# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.IMessageReceiver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Interface for message receivers.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class IMessageReceiver:
    """
    Callback interface to receive incoming messages.

    Example:
        class MyMessageReceiver(IMessageReceiver):
            def receive_message(self, envelop, queue):
                print "Received message: " + envelop.getMessageAsString()

        messageQueue = MemoryMessageQueue()
        messageQueue.listen("123", MyMessageReceiver())

        messageQueue.open("123")
        messageQueue.send("123", MessageEnvelop(None, "mymessage", "ABC")) // Output in console: "ABC"
    """
    def receive_message(self, message, queue):
        raise NotImplementedError('Method from interface definition')
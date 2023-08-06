# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MessageEnvelop
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Message envelop implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services3_commons.convert import StringConverter
from pip_services3_commons.data import IdGenerator

class MessageEnvelop(object):
    """
    Allows adding additional information to messages. A correlation id, message id, and a message type
    are added to the data being sent/received. Additionally, a MessageEnvelope can reference a lock token.

    Side note: a MessageEnvelope's message is stored as a buffer, so strings are converted using utf8 conversions.
    """
    reference = None
    message_id = None
    message_type = None
    correlation_id = None
    message = None
    # reference = None

    def __init__(self, correlation_id = None, message_type = None, message = None):
        """
        Creates a new MessageEnvelope, which adds a correlation id, message id, and a type to the
        data being sent/received.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_type: a string value that defines the message's type.

        :param message: the data being sent/received.
        """
        self.correlation_id = correlation_id
        self.message_type = message_type
        self.message = message
        self.message_id = IdGenerator.next_long()

    def __getstate__(self):
        """
        :return: the lock token that this MessageEnvelope references.
        """
        state = self.__dict__.copy()
        del state['reference']
        return state

    def __setstate__(self, state):
        """
        Sets a lock token reference for this MessageEnvelope.

        :param state: the lock token to reference.
        """
        self.__dict__.update(state)

    def __str__(self):
        """
        Convert's this MessageEnvelope to a string, using the following format:
        <code>"[<correlation_id>,<message_type>,<message.toString>]"</code>.
        If any of the values are <code>null</code>, they will be replaced with <code>---</code>.

        :return: the generated string.
        """
        output = "[" 
        output += self.correlation_id if self.correlation_id != None else "---"
        output += "," 
        output += self.message_type if self.message_type != None else "---" 
        output += ","
        output += StringConverter.to_string(self.message) if self.message != None else "--"
        output += "]"
        return output

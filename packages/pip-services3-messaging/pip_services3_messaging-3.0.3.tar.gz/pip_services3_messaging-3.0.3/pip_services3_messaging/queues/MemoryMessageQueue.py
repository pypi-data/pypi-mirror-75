# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MemoryMessageQueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Memory message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading

from pip_services3_commons.run import ICleanable
from .MessageEnvelop import MessageEnvelop
from .MessagingCapabilities import MessagingCapabilities
from .MessageQueue import MessageQueue

class MemoryMessageQueue(MessageQueue, ICleanable):
    """
    Message queue that sends and receives messages within the same process by using shared memory.
    This queue is typically used for testing to mock real queues.

    ### Configuration parameters ###

        - name:                        name of the message queue

    ### References ###

        - *:logger:*:*:1.0           (optional) ILogger components to pass log messages
        - *:counters:*:*:1.0         (optional) ICounters components to pass collected measurements

    Example:
        queue = MessageQueue("myqueue")
        queue.send("123", MessageEnvelop(None, "mymessage", "ABC"))

        message = queue.receive("123", 0)
        if message != None:
            ...
            queue.complete("123", message)
    """
    _default_lock_timeout = 30000
    _default_wait_timeout = 5000

    _event = None
    _messages = None
    _lock_token_sequence = 0
    _locked_messages = None
    _listening = None
    _opened = False

    class LockedMessage(object):
        #message = None
        lock_expiration = None


    def __init__(self, name = None):
        """
        Creates a new instance of the message queue.

        :param name: (optional) a queue name.
        """
        super(MemoryMessageQueue, self).__init__(name)
        self._event = threading.Event()
        self._capabilities = MessagingCapabilities(True, True, True, True, True, True, True, False, True)

        self._messages = []
        self._locked_messages = {}


    def is_opened(self):
        """
        Checks if the component is opened.

        :return: true if the component has been opened and false otherwise.
        """
        return self._opened

    def _open_with_params(self, correlation_id, connection, credentials):
        """
        Opens the component with given connection and credential parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param connection: connection parameters

        :param credentials: credential parameters
        """
        self._opened = True
        self._logger.trace(correlation_id, "Opened queue " + str(self))


    def close(self, correlation_id):
        """
        Closes component and frees used resources.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._opened = False
        self._listening = False 
        self._event.set()
        self._logger.trace(correlation_id, "Closed queue " + str(self))


    def read_message_count(self):
        """
        Reads the current number of messages in the queue to be delivered.

        :return: a number of messages
        """
        self._lock.acquire()
        try:
            return len(self._messages)
        finally:
            self._lock.release()


    def send(self, correlation_id, message):
        """
        Sends a message into the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param envelop: a message envelop to be sent.
        """
        if message == None: return

        self._lock.acquire()
        try:
            # Add message to the queue
            self._messages.append(message)
        finally:
            self._lock.release()

        # Release threads waiting for messages
        self._event.set()
        
        self._counters.increment_one("queue." + self.get_name() + ".sent_messages")
        self._logger.debug(correlation_id, "Sent message " + str(message) + " via " + str(self))


    def peek(self, correlation_id):
        """
        Peeks a single incoming message from the queue without removing it.
        If there are no messages available in the queue it returns null.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :return: a message object.
        """
        message = None

        self._lock.acquire()
        try:
            # Pick a message
            if len(self._messages) > 0:
                message = self._messages[0]
        finally:
            self._lock.release()

        if message != None:
            self._logger.trace(correlation_id, "Peeked message " + str(message) + " on " + str(self))

        return message


    def peek_batch(self, correlation_id, message_count):
        """
        Peeks multiple incoming messages from the queue without removing them.
        If there are no messages available in the queue it returns an empty list.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_count: a maximum number of messages to peek.

        :return: a list of message objects.
        """
        messages = []

        self._lock.acquire()
        try:
            index = 0
            while index < len(self._messages) and index < message_count:
                messages.append(self._messages[index])
                index += 1
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Peeked " + str(len(messages)) + " messages on " + str(self))

        return messages


    def receive(self, correlation_id, wait_timeout):
        """
        Receives an incoming message and removes it from the queue.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param wait_timeout: a timeout in milliseconds to wait for a message to come.

        :return: a message object.
        """
        message = None

        self._lock.acquire()
        try:
            # Try to get a message
            if len(self._messages) > 0:
                message = self._messages[0]
                del self._messages[0]
            else:
                self._event.clear()
        finally:
            self._lock.release()

        if message == None:
            self._event.wait(wait_timeout)

        self._lock.acquire()
        try:
            # Try to get a message again
            if message == None and len(self._messages) > 0:
                message = self._messages[0]
                del self._messages[0]
            
            # Exit if message was not found
            if message == None:
                return None

            # Generate and set locked token
            locked_token = self._lock_token_sequence
            self._lock_token_sequence += 1
            message.reference = locked_token

            # Add messages to locked messages list
            locked_message = self.LockedMessage()
            locked_message.lock_expiration = time.perf_counter() + (float(self._default_lock_timeout) / 1000.)
            #locked_message.message = message

            self._locked_messages[locked_token] = locked_message
        finally:
            self._lock.release()

        self._counters.increment_one("queue." + self.get_name() + ".received_messages")
        self._logger.debug(message.correlation_id, "Received message " + str(message) + " on " + str(self))

        return message


    def renew_lock(self, message, lock_timeout):
        """
        Renews a lock on a message that makes it invisible from other receivers in the queue.
        This method is usually used to extend the message processing time.

        :param message: a message to extend its lock.

        :param lock_timeout: a locking timeout in milliseconds.
        """
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            # Get message from locked queue
            locked_token = message.reference
            locked_message = self._locked_messages[locked_token]

            # If lock is found, extend the lock
            if locked_message != None:
                locked_message.lock_expiration = time.perf_counter() + (float(lock_timeout) / 1000.)
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Renewed lock for message " + str(message) + " at " + str(self))


    def abandon(self, message):
        """
        Returnes message into the queue and makes it available for all subscribers to receive it again.
        This method is usually used to return a message which could not be processed at the moment
        to repeat the attempt. Messages that cause unrecoverable errors shall be removed permanently
        or/and send to dead letter queue.

        :param message: a message to return.
        """
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            # Get message from locked queue
            locked_token = message.reference
            locked_message = self._locked_messages[locked_token]
            if locked_message != None:
                # Remove from locked messages
                del self._locked_messages[locked_token]
                message.reference = None

                # Skip if it is already expired
                if locked_message.lock_expiration <= time.perf_counter():
                    return
            # Skip if it absent
            else:
                return
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Abandoned message " + str(message) + " at " + str(self))

        # Add back to the queue
        self.send(message.correlation_id, message)


    def complete(self, message):
        """
        Permanently removes a message from the queue.
        This method is usually used to remove the message after successful processing.

        :param message: a message to remove.
        """
        if message == None or message.reference == None: 
            return

        self._lock.acquire()
        try:
            lock_key = message.reference
            del self._locked_messages[lock_key]
            message.reference = None
        finally:
            self._lock.release()

        self._logger.trace(message.correlation_id, "Completed message " + str(message) + " at " + str(self))


    def move_to_dead_letter(self, message):
        """
        Permanently removes a message from the queue and sends it to dead letter queue.

        :param message: a message to be removed.
        """
        if message == None or message.reference == None:
            return

        self._lock.acquire()
        try:
            lock_key = message.reference
            del self._locked_messages[lock_key]
            message.reference = None
        finally:
            self._lock.release()

        self._counters.increment_one("queue." + self.get_name() + ".dead_messages")
        self._logger.trace(message.correlation_id, "Moved to dead message " + str(message) + " at " + str(self))


    def listen(self, correlation_id, receiver):
        """
        Listens for incoming messages and blocks the current thread until queue is closed.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        if self._listening:
            self._logger.error(correlation_id, "Already listening queue " + str(self))
            return
        
        self._logger.trace(correlation_id, "Started listening messages at " + str(self))

        self._listening = True

        while self._listening:
            message = self.receive(correlation_id, self._default_wait_timeout)

            if self._listening and message != None:
                try:
                    receiver.receive_message(message, self)
                except Exception as ex:
                    self._logger.error(correlation_id, ex, "Failed to process the message")
                    #self.abandon(message)
        
        self._logger.trace(correlation_id, "Stopped listening messages at " + str(self))


    def end_listen(self, correlation_id):
        """
        Ends listening for incoming messages.
        When this method is call [[listen]] unblocks the thread and execution continues.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._listening = False


    def clear(self, correlation_id):
        """
        Clears component state.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self._lock.acquire()
        try:
            # Clear messages
            self._messages = []
            self._locked_messages = {}
        finally:
            self._lock.release()

        self._logger.trace(correlation_id, "Cleared queue " + str(self))


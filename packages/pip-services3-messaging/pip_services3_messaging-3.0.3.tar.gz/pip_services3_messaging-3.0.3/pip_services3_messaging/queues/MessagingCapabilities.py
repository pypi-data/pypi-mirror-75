# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MessagingCapabilities
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Messaging capabilities implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

class MessagingCapabilities(object):
    """
    Data object that contains supported capabilities of a message queue.
    If certain capability is not supported a queue will throw NotImplemented exception.
    """
    _message_count = None
    _send = None
    _receive = None
    _peek = None
    _peek_batch = None
    _renew_lock = None
    _abandon = None
    _dead_letter = None
    _clear = None

    def __init__(self, message_count, send, receive, peek, peek_batch, renew_lock, abandon, dead_letter, clear):
        """
        Creates a new instance of the capabilities object.

        :param message_count: true if queue supports reading message count.

        :param send: true if queue is able to send messages.

        :param receive: true if queue is able to receive messages.

        :param peek: true if queue is able to peek messages.

        :param peek_batch: true if queue is able to peek multiple messages in one batch.

        :param renew_lock: true if queue is able to renew message lock.

        :param abandon: true if queue is able to abandon messages.

        :param dead_letter: true if queue is able to send messages to dead letter queue.

        :param clear: true if queue can be cleared.
        """
        self._message_count = message_count
        self._send = send
        self._receive = receive
        self._peek = peek
        self._peek_batch = peek_batch
        self._renew_lock = renew_lock
        self._abandon = abandon
        self._dead_letter = dead_letter
        self._clear = clear

    def can_message_count(self):
        """
        Informs if the queue is able to read number of messages.

        :return: true if queue supports reading message count.
        """
        return self._message_count

    def can_send(self):
        """
        Informs if the queue is able to send messages.

        :return: true if queue is able to send messages.
        """
        return self._send

    def can_receive(self):
        """
        Informs if the queue is able to receive messages.

        :return: true if queue is able to receive messages.
        """
        return self._receive

    def can_peek(self):
        """
        Informs if the queue is able to peek messages.

        :return: true if queue is able to peek messages.
        """
        return self._peek

    def can_peek_batch(self):
        """
        Informs if the queue is able to peek multiple messages in one batch.

        :return: true if queue is able to peek multiple messages in one batch.
        """
        return self._peek_batch

    def can_renew_lock(self):
        """
        Informs if the queue is able to renew message lock.

        :return: true if queue is able to renew message lock.
        """
        return self._renew_lock

    def can_abandon(self):
        """
        Informs if the queue is able to abandon messages.

        :return: true if queue is able to abandon.
        """
        return self._abandon

    def can_dead_letter(self):
        """
        Informs if the queue is able to send messages to dead letter queue.

        :return: true if queue is able to send messages to dead letter queue.
        """
        return self._dead_letter

    def can_clear(self):
        """
        Informs if the queue can be cleared.

        :return: true if queue can be cleared.
        """
        return self._clear

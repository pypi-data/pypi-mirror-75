# -*- coding: utf-8 -*-
"""
    pip_services3_messaging.queues.MessageQeueue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Abstract message queue implementation.
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

import threading

from pip_services3_commons.config import IConfigurable, NameResolver
from pip_services3_commons.refer import IReferenceable
from pip_services3_commons.run import IOpenable, IClosable
from pip_services3_components.log import CompositeLogger
from pip_services3_components.count import CompositeCounters
from pip_services3_components.auth import CredentialResolver
from pip_services3_components.connect import ConnectionResolver

from .MessageEnvelop import MessageEnvelop
from .IMessageQueue import IMessageQueue

class MessageQueue(IConfigurable, IReferenceable, IMessageQueue):
    """
    Abstract message queue.

    Abstract message queue that is used as a basis for specific message queue implementations.

    ### Configuration parameters ###

        - name:                        name of the message queue
        - connection(s):
            - discovery_key:             key to retrieve parameters from discovery service
            - protocol:                  connection protocol like http, https, tcp, udp
            - host:                      host name or IP address
            - port:                      port number
            - uri:                       resource URI or connection string with all parameters in it
        - credential(s):
        - store_key:                 key to retrieve parameters from credential store
        - username:                  user name
        - password:                  user password
        - access_id:                 application access id
        - access_key:                application secret key

    ### References ###

        - *:logger:*:*:1.0           (optional) ILogger components to pass log messages
        - *:counters:*:*:1.0         (optional) ICounters components to pass collected measurements
        - *:discovery:*:*:1.0        (optional) IDiscovery components to discover connection(s)
        - *:credential-store:*:*:1.0 (optional) ICredentialStore componetns to lookup credential(s)
    """
    _name = None
    _capabilities = None
    _lock = None
    _logger = None
    _counters = None
    _credential_resolver = None
    _connection_resolver = None

    def __init__(self, name = None):
        """
        Creates a new instance of the message queue.

        :param name: (optional) a queue name
        """
        self._lock = threading.Lock()
        self._logger = CompositeLogger()
        self._counters = CompositeCounters()
        self._connection_resolver = ConnectionResolver()
        self._credential_resolver = CredentialResolver()
        self._name = name


    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._name = NameResolver.resolve(config)
        self._logger.configure(config)
        self._credential_resolver.configure(config)
        self._connection_resolver.configure(config)


    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)
        self._counters.set_references(references)
        self._credential_resolver.set_references(references)
        self._connection_resolver.set_references(references)


    def open(self, correlation_id):
        """
        Opens the component.

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        connection = self._connection_resolver.resolve(correlation_id)
        credential = self._credential_resolver.lookup(correlation_id)
        self._open_with_params(correlation_id, connection, credential)


    def _open_with_params(self, correlation_id, connection, credential):
        """
        Opens the component with given connection and credential parameters.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param connection: connection parameters

        :param credential: credential parameters
        """
        raise NotImplementedError('Abstract method that shall be overriden')


    def get_name(self):
        """
        Gets the queue name

        :return: the queue name.
        """
        return self._name if self._name != None else "undefined"


    def get_capabilities(self):
        """
        Gets the queue capabilities

        :return: the queue's capabilities object.
        """
        return self._capabilities


    def send_as_object(self, correlation_id, message_type, message):
        """
        Sends an object into the queue.
        Before sending the object is converted into JSON string and wrapped in a [[MessageEnvelop]].

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param message_type: a message type

        :param message: an object value to be sent
        """
        envelop = MessageEnvelop(correlation_id, message_type, message)
        self.send(correlation_id, envelop)


    def begin_listen(self, correlation_id, receiver):
        """
        Listens for incoming messages without blocking the current thread.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param receiver: a receiver to receive incoming messages.
        """
        # Start listening on a parallel tread
        thread = threading.Thread(target=self.listen, args=(correlation_id, receiver))
        thread.daemon = True
        thread.start()

    def __str__(self):
        """
        Gets a string representation of the object.

        :return: a string representation of the object.
        """
        return "[" + self.get_name() + "]"

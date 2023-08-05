# default lib imports
import logging
import ssl
import sys
import os
import socket

# external lib imports
import gevent

# module imports
from .Client import Client
from .Packet import Packet
from .Message import Message
from .DeviceType import DeviceType


# Manager class
class Manager:
    def __init__(self, ssl_context: ssl.SSLContext = None, host: str = "127.0.0.1", connection_port: int = 8595,
                 max_workers: int = 8, heartbeat_rate: int = 60, heartbeat_timeout: int = 10,
                 backlogged_connections: int = 10,
                 logging_id: str = "[Manager]", logging_level: int = logging.WARNING,
                 client_logging_level: int = logging.WARNING):

        # <> Instantiate Public Class Variables <>
        # the host is the computer running this program
        self.host = host

        # port that the manager will listen on for devices that want to connect
        self.port = connection_port

        # the delay between heartbeat messages
        if isinstance(heartbeat_rate, (int, float)):
            self.heartbeat_rate = heartbeat_rate
        else:
            raise TypeError("heartbeat_rate must be a number representing delay in seconds")

        # the time a client has to respond before being removed
        if isinstance(heartbeat_timeout, (int, float)):
            self.heartbeat_timeout = heartbeat_timeout
        else:
            raise TypeError("heartbeat_timeout must be a number representing time in seconds")

        # <> Instantiate Private Class Variables <>
        # socket that will be used for accepting new clients
        self.__connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # a pool of connected clients
        self.__client_pool = []

        # a list of device types
        self.__device_types = {}

        # logger object and setup
        if isinstance(logging_id, str):
            # logger object
            self.logger = logging.getLogger(logging_id)
        else:
            raise TypeError("logging_id must be of type str")

        if isinstance(logging_level, int):
            self.logger.setLevel(logging_level)
        else:
            raise TypeError("logging_level must resolve to an integer value")

        if isinstance(client_logging_level, int):
            self.client_logging_level = client_logging_level
        else:
            raise TypeError("client_logging_level must resolve to an integer value")

        # <> Server Socket Setup <>
        # true if the socket is using SSL
        self.__ssl_enabled = False

        # attempt to bind the socket to the provided host and port
        try:
            # try binding
            self.__connection_socket.bind((self.host, self.port))

        # in the case a socket error is raised
        except socket.error:
            raise Exception("Unable to bind server socket to the provided host and port")

        # attempt to set the socket as a listening socket
        try:
            # if the backlogged_connections is not type int then raise an exception
            if not isinstance(backlogged_connections, int):
                raise TypeError("backlogged_connections must be type int")

            # set the socket as a listening socket
            self.__connection_socket.listen(backlogged_connections)

        # in the case a socket error is raised
        except socket.error:
            raise Exception("Unable to set the socket as ")

        # if a SSL context is provided then try and wrap the socket
        if ssl_context is not None and isinstance(ssl_context, ssl.SSLContext):
            # try to use the SSL context provided
            try:
                # create a SSLSocket using the provided ssl_context
                self.__connection_socket = \
                    ssl_context.wrap_socket(self.__connection_socket, server_side=True)

                # set __ssl_enabled as true
                self.__ssl_enabled = True

                # logging output
                self.logger.info("(Constructor) Provided SSL context used to wrap socket successfully.")

            # in the case of a SSLError
            except ssl.SSLError as error:
                # logging output
                self.logger.error("(Constructor)  Unable to create SSL socket using the provided SSL context due to the"
                                  + " following SSLError: " + str(error) + ". Defaulting to the depreciated"
                                  + " ssl.wrap_socket() method. Do not use this in a production application.")

                # use the default ssl.wrap_socket method
                self.__connection_socket = ssl.wrap_socket(self.__connection_socket)

                # set __ssl_enabled as true
                self.__ssl_enabled = True

        # if the ssl_context provided
        elif ssl_context is not None and not isinstance(ssl_context, ssl.SSLContext):
            # logging output
            self.logger.error("(Constructor) ssl_context is not the proper type, please provide a sll.SSLContext."
                              + " Defaulting to the depreciated ssl.wrap_socket() method. Do not use this in a"
                              + " production application.")

            # use the default ssl.wrap_socket method
            self.__connection_socket = ssl.wrap_socket(self.__connection_socket)

            # set __ssl_enabled as true
            self.__ssl_enabled = True

        # <> Greenlet Setup and Initialization <>
        # a gevent ThreadPool which will be used when the manager needs to create temporary greenlets
        self.__executor = gevent.get_hub().threadpool

    # run on a greenlet and is what connects new devices to the manager
    def __connection_listener(self):
        # log on init
        self.logger.debug("(Connection Listener) Starting process...")

        while True:
            try:
                # await a connection to the socket waiting for clients
                client_connection, client_address = self.__connection_socket.accept()

                # logging output
                self.logger.info("(Connection Listener) New Client Connection Established. Client IP Address: '"
                                 + str(client_address[0]) + "'")

                # hand over the client connection and address to a temporary greenlet which will get the data of the new
                # client
                self.__executor.spawn(self.__register_client, client_connection, client_address)

            # catch any SSL errors and let the user know about them so they can fix them on the client end
            except ssl.SSLError as exception:
                self.logger.error("(Connection Listener) Error occurred in the connection_listener greenlet."
                                  " Exception: " + str(exception))
            finally:
                # yield greenlet
                gevent.sleep(0.1)

    # takes a client socket and address and awaits the data which identifies the client's type
    def __register_client(self, connection: socket, address: tuple):
        try:
            # try to create the client while checking for errors
            try:
                # create the client object (will also retrieve the client's info)
                client = Client(connection, address, self.client_logging_level)

                # get the client's info
                client.get_data()

                # logging output
                self.logger.info("(Client Registrar) Got the data of client '" + client.uuid
                                 + "', adding client to pool.")

            # in the case the client gave an invalid type
            except Client.InvalidInfo:
                # logging output
                self.logger.error("(Client Registrar) Failed to receive valid data from client client with IP '"
                                  + str(address[0]) + "', ending connection.")

                # exit the function early
                return

            # check if a client is already connected which shares a UUID, assume that it is a invalid connection of the
            # client which is trying to reconnect and remove the old connection
            # go through all clients
            for index, check_client in enumerate(self.__client_pool):
                # check and see if the current client's UUID matches that of another client
                if check_client.uuid == client.uuid:
                    # logging output
                    self.logger.debug("(Client Registrar) Client with UUID '" + client.uuid + "' has overridden a"
                                      + " established connection. This was likely due to reconnection before a "
                                      + "heartbeat check but could also be caused by two clients sharing a UUID.")

                    # try to end the old client to end its connection if it still exists for some reason
                    try:
                        # send the checked client the end message
                        check_client.end()
                    finally:
                        # remove the client
                        self.__remove_client(check_client)

            # catch and exceptions within the general on_connect function
            try:
                # run the on_connect function for the client
                self.on_connect(client)

            # in case of a exception when executing handler
            except Exception as error:
                self.logger.error(
                    "(Client Registrar) Exception caught when running the on_connect() handler. Exception: '"
                    + str(error) + "'")

            # catch and exceptions within the device specific on_message function if any occur
            try:
                # check if the user provided a device specific handler for this client's device type, if so execute it
                if client.type in self.__device_types.keys():
                    self.__device_types[client.type].on_connect(client)

            # in case of a exception when executing handler
            except Exception as error:
                self.logger.error(
                    "(Client Registrar) Exception caught when running the on_connect() handler. For the " + client.type +
                    " client type. Exception: '" + str(error) + "'")

            # add the client to the pool
            self.__client_pool.append(client)

            # log the success
            self.logger.info("(Client Registrar) Client with UUID '" + client.uuid + "' successfully added to pool.")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_tb.tb_lineno)
            self.logger.warning("EXCEPTION IN REGISTRAR: " + str(e))

    # heartbeat loop for checking if clients are still connected, run every x seconds based on the heartbeat_rate
    def __heartbeat_checker(self):
        # log on init
        self.logger.debug("(Heartbeat Checker) Starting process...")

        while True:
            # wait the delay for a heartbeat to be sent
            gevent.sleep(self.heartbeat_rate)

            # logging output
            self.logger.info("(Heartbeat Checker) Starting client heartbeat check. Number of clients: '"
                             + str(len(self.__client_pool)) + "'.")

            # check the heartbeat of the connected clients
            for index in range(len(self.__client_pool) - 1, -1, -1):
                # logging output
                self.logger.debug("(Heartbeat Checker) Checking the heartbeat of client '"
                                  + self.__client_pool[index].uuid + "'.")

                # submit the heartbeat check to the executor
                self.__executor.spawn(self.__heartbeat, index)

    # check the heartbeat of a client based on their given index
    def __heartbeat(self, client_index):
        client = self.__client_pool[client_index]

        # logging output
        self.logger.debug("(Heartbeat Checker for Client '" + client.uuid
                          + "') Initiating heartbeat check.")

        try:
            # check the heartbeat of the client
            client.heartbeat(self.heartbeat_timeout)

            # logging output
            self.logger.debug("(Heartbeat Checker for Client '" + client.uuid + "') Client passed heartbeat check.")

            return
        except Client.ConnectionEnd:
            try:
                # end the client's connection
                client.end()
            finally:
                # logging output
                self.logger.error("(Heartbeat Checker for Client '" + client.uuid
                                  + "') Client failed heartbeat check, removing from pool.")

                # remove the client
                self.__remove_client(client)

    # this loop checks for client messages to the server
    def __message_listener(self):
        # log on init
        self.logger.debug("(Message Listener) Starting process...")

        # loop for the lifetime of the program
        while True:
            # loop through each client
            for client in self.__client_pool:
                # check if the client has sent some data
                packet = client.recv(0)

                # if the client has sent no data move onto the next client
                if packet is None:
                    continue
                # if the client has sent some data then process it using the on_message function
                else:
                    # logging message
                    self.logger.debug("(Message Listener) Data received from client '" + client.uuid + "'."
                                      + " Sending data to appropriate handlers.")

                    # create a message
                    message = Message(client, packet)

                    # submit data to the __handle_message function
                    self.__executor.spawn(self.__handle_message(message))

            # yield
            gevent.sleep(0.1)

    # function which is used to handle data sent from the client
    def __handle_message(self, message: Message):
        # catch and exceptions within the general on_message function
        # noinspection PyBroadException
        try:
            # run the on_connect function for the client
            self.on_message(message)

        # in case of a exception when executing handler
        except Exception as error:
            self.logger.error("(Message Handler) Exception caught when running the on_message() handler. Exception: '"
                              + str(error) + "'")

        # catch and exceptions within the device specific on_message function if any occur
        # noinspection PyBroadException
        try:
            # check if the user provided a device specific handler for this client's device type, if so execute it
            if message.client.type in self.__device_types.keys():
                self.__device_types[message.client.type].on_message(message)

        # in case of a exception when executing handler
        except Exception as error:
            self.logger.error(
                "(Message Handler) Exception caught when running the on_message() handler for DeviceType '" +
                message.client.type + "." + "Exception: '" + str(error) + "'")

    # remove a client from the client pool and trigger the disconnect handler
    def __remove_client(self, client):
        # catch and exceptions within the general on_connect function
        try:
            # run the on_connect function for the client
            self.on_disconnect(client)

        # in case of a exception when executing handler
        except Exception as error:
            self.logger.error(
                "(Message Handler) Exception caught when running the on_disconnect() handler. Exception: '"
                + str(error) + "'")

        # catch and exceptions within the device specific on_message function if any occur
        try:
            # check if the user provided a device specific handler for this client's device type
            # if so execute it
            if client.type in self.__device_types.keys():
                self.__device_types[client.type].on_disconnect(client)

        # in case of a exception when executing handler
        except Exception as error:
            self.logger.error(
                "(Message Handler) Exception caught when running the on_disconnect() handler. For the " +
                client.type + " client type. Exception: '" + str(error) + "'")

        # remove item from list
        self.__client_pool = [x for x in self.__client_pool if x.instance_id != client.instance_id]

    # sends data to all clients
    def send_all(self, data):
        # for each client in the pool
        for client in self.__client_pool:
            # send the client the data
            self.__executor.spawn(client.send, data)

    # sends data to all clients of a specified device_type
    def send_type(self, device_type, packet: Packet):
        # for each client in the pool
        for client in self.__client_pool:
            # check if the client matches the provided type
            if client.type == device_type:
                # send the client the data
                self.__executor.spawn(client.send, packet)

    # sends data to a client given a uuid
    def send(self, unique_id, packet: Packet):
        # for each client in the pool
        for client in self.__client_pool:
            # check if the client matches the provided uuid
            if client.uuid == unique_id:
                # send the client the data
                self.__executor.spawn(client.send, packet)
                return

    # returns an list of dictionaries storing the connected clients' information
    def get_client_data(self):
        # data list
        info = []

        # loop through the clients and add their info to the list
        for client in self.__client_pool:
            # add the info for the given client
            info.append(client.return_data())

        # return the list of client data
        return info

    # event manager decorator function
    def event(self, coroutine):
        # handle general on_connect and on_message handlers
        if coroutine.__name__ == "on_connect" or coroutine.__name__ == "on_message":
            # logging output
            self.logger.info("(Event Handler) '" + coroutine.__name__ + "' handler was added successfully.")

            # replaces the existing coroutine with the provided one
            setattr(self, coroutine.__name__, coroutine)
            return True

    # used to add a device to the manager
    def add_device(self, device: DeviceType):
        # ensure the device is of type DeviceType
        if not isinstance(device, DeviceType):
            raise ValueError("device is not of type DeviceType")

        # ensure device.type is of type str
        if not isinstance(device.type, str):
            raise ValueError("device.type is not of type str")

        # add the device to the list of device types
        self.__device_types.update({device.type: device})

        # logging output
        self.logger.debug("(Device Adder) Successfully added DeviceType '" + device.type + "' to the manager.")

    # on connection function - run on client connection
    def on_connect(self, client: Client):
        return

    # on message function - runs when a client sends a message to the server
    def on_message(self, message: Message):
        return

    # on disconnect function - runs when the client disconnects from the server
    def on_disconnect(self, client: Client):
        return

    # runs all the handlers
    def __process_handler(self):
        # logging output
        self.logger.info("(Process Handler) Starting processes.")

        # add the core threads to the pool
        self.__executor.spawn(self.__connection_listener)
        self.__executor.spawn(self.__heartbeat_checker)
        self.__executor.spawn(self.__message_listener)

        # logging output
        self.logger.info("(Process Handler) All processes started.")
        return

    # starts all of the necessary permanent background threads
    def start(self):
        # start all of the background threads
        self.__process_handler()

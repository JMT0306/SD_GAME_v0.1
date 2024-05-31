import logging

import server_impl as server
from server_impl.gamemech import GameMech
from socket_impl.sockets import Socket
from server_impl import LOG_FILENAME
from server_impl import LOG_LEVEL
from server_impl import SERVER_ADDRESS
from server_impl import PORT
from server_shared_state import ServerSharedState
import client_server

#---------------------------- starting class --------------------------------
class GameServerSkeleton:
#    def __init__(self, gamemech:GameMech) -> None:
    def __init__(self, shared_state:ServerSharedState) -> None:

        """
        Creates a client given the server server to use
        """
        # Keeps information about the execution of the program
        logging.basicConfig(filename=LOG_FILENAME,
                            level=LOG_LEVEL,
                            format='%(asctime)s (%(levelname)s): %(message)s')
        self.shared_state = shared_state
        #self.gamemech = gamemech
    # ------------------- server execution -------------------------------------
    def run(self) -> None:
        """
        Runs the server server until the client sends a "terminate" action
        """
        socket= Socket.create_server_connection(SERVER_ADDRESS, PORT)

        logging.info("Waiting for clients to connect on port " + str(socket.port))
        keep_running = True
        # While keep_running, get connections and then interact with the client connected
        while keep_running:
            current_connection, address = socket.server_connect()
            logging.debug("Client " + str(address) + " just connected")
            #client_server.ClientThread(self.gamemech,current_connection, address).start()
            client_server.ClientThread(self.shared_state,current_connection, address).start()

            # While client connected, wait for its demmands and dispatch the requests
            # with current_connection:
            #    last_request = False
            #    #If it is not the last request receive the request
            #    while not last_request:
            #        keep_running, last_request = self.dispatch_request()
            #    #If it is the last request, client is disconnecting...
            #    logging.debug("Client " + str(address) + " disconnected")
        #If it is not keep_running than socket must be closed...
        self.socket.close()
        logging.info("Server stopped")
#---------------------------- end of class --------------------------------

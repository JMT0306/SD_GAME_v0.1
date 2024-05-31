import numpy
from socket_impl.sockets import Socket
import stub as client

class ClientStub:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self.socket = Socket.create_client_connection(self._host, self._port)

    def get_nr_quad_x(self) -> int:
        self.socket.send_str(client.QUADX_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def get_nr_quad_y(self) -> int:
        self.socket.send_str(client.QUADY_OP)
        return self.socket.receive_int(client.INT_SIZE)

    #new - protocol for setting player and receiving id
    def set_player(self, name:str) -> tuple:
        self.socket.send_str(client.PLAYER_OP)
        self.socket.send_str(name)
        # It will receive a tuple
        return self.socket.receive_obj(client.INT_SIZE)

    # new - protocol to start the game
    def execute_start_game(self) -> int:
        self.socket.send_str(client.START_GAME)
        return self.socket.receive_int(client.INT_SIZE)

    # new - protocol for updating position
    def get_objects(self) -> dict:
        self.socket.send_str(client.GET_OBJTS)
        return self.socket.receive_obj(client.INT_SIZE)

    def step(self,id: int, dir: int) -> tuple:
        self.socket.send_str(client.STEP_OP)
        self.socket.send_int(id, client.INT_SIZE)
        self.socket.send_int(dir, client.INT_SIZE)
        # It will receive a tuple
        return self.socket.receive_obj(client.INT_SIZE)
    def collect_item(self, player_id: int, item_id: int) -> None:
        self.socket.send_str(client.COLLECT_ITEM_OP)
        self.socket.send_int(player_id, client.INT_SIZE)
        self.socket.send_int(item_id, client.INT_SIZE)

    # def execute(self,id: int, dir: int) -> tuple:
    #     self.socket.send_str(client.UPDATE_OP)
    #     self.socket.send_int(id, client.INT_SIZE)
    #     self.socket.send_int(dir, client.INT_SIZE)
    #     # It will receive a tuple
    #     return self.socket.receive_obj(client.INT_SIZE)

    # new - protocol for getting walls
    def get_walls(self) -> dict:
        self.socket.send_str(client.GET_WALLS_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def exec_stop_client(self):
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self):
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()


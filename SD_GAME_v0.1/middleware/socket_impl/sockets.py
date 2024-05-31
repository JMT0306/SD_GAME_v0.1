import socket
import json
import server_impl

#
# Existem duas funções estáticas que permitem criar os sockets no lado do cliente e do servidor.
# Elas retornam uma instância da classe Socket, permitindo depois usar esse objeto criado para
# chamar as funções.
# Na função server_connect, é criado um novo socket que vai responsabilizar-se por interagir
# com o cliente.
# A alternativa a este desenho seria ter uma função no main de cada um dos lados, chamando estas funções.
class Socket:
    def __init__(self, connection, port):
        self._current_connection = connection
        self._port = port

    @property
    def port(self):
        return self._port

    def get_address(self):
        return self._current_connection.getpeername()


    @property
    def current_connection(self):
        return self._current_connection

    def receive_int(self, n_bytes: int) -> int:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next integer read from the current connection
        """
        data = self._current_connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, value: int, n_bytes: int) -> None:
        """
        :param value: The integer value to be sent to the current connection
        :param n_bytes: The number of bytes to send
        """
        self._current_connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = self._current_connection.recv(n_bytes)
        return data.decode()

    def send_str(self, value: str) -> None:
        """
        :param value: The string value to send to the current connection
        """
        self._current_connection.send(value.encode())

    def send_obj(self,value: object, n_bytes:int)-> None:
        msg = json.dumps(value)
        #print("SEND_OBJ:",msg)
        size = len(msg)
        self.send_int(size, n_bytes)
        self.send_str(msg)

    def receive_obj(self, n_bytes: int) -> object:
        size  = self.receive_int(n_bytes)
        obj =  self.receive_str(size)
        return json.loads(obj)

    def close(self):
        self._current_connection.close()
        self._current_connection = None



    def server_connect(self) -> tuple:
        connection, address = self._current_connection.accept()
        return (Socket(connection, self._port), address)

#    def __enter__(self):
#        return self

#    def __exit__(self, exc_type, exc_val, exc_tb):
#        self.close()


    @staticmethod
    def create_server_connection(host:str, port:int):
        connection = socket.socket()
        connection.bind((host, port))
        connection.listen(1)
        return Socket(connection, port)

    @staticmethod
    def create_client_connection(host:str, port:int):
        connection = socket.socket()
        connection.connect((host, port))
        return Socket(connection, port)

    #def bind(self) -> None:
    #    # Connecting as a server
    #    self._s = socket.socket()
    #    self._s.bind(('', self._port))

    #def listen(self) -> None:
    #    self._s.listen(1)


#    def connect(self) -> None:
#        self._current_connection = socket.socket()
#        self._current_connection.connect((self._host, self._port))



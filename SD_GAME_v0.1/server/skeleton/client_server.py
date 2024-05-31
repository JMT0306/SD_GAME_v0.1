from threading import Thread
import logging
import time

from server_impl.gamemech import GameMech
import server_impl as server
from server_shared_state import ServerSharedState

class ClientThread(Thread):
    def __init__(self, shared_state: ServerSharedState, current_connection, address):
        self.current_connection = current_connection
        self.shared_state = shared_state
        self.gamemech = self.shared_state.gamemech()
        self.address = address
        self.last_get_objects_time = time.time()
        Thread.__init__(self)

    def process_objects(self):
        try:
            objects = self.shared_state.get_objects()
            self.current_connection.send_obj(objects, server.INT_SIZE)
            print(f"Sent objects: {objects}")
        except Exception as e:
            print(f"Error processing objects: {e}")

    def process_step(self):
        try:
            id = self.current_connection.receive_int(server.INT_SIZE)
            dir = self.current_connection.receive_int(server.INT_SIZE)
            res = self.gamemech.execute(id, dir)
            self.current_connection.send_obj(res, server.INT_SIZE)
            self.shared_state.update_objects()  # Atualiza o estado compartilhado com as novas posições dos jogadores
        except Exception as e:
            print(f"Error processing step: {e}")

    def process_add_player(self):
        try:
            name = self.current_connection.receive_str(server.MAX_STR_SIZE)
            res = self.gamemech.add_player(name)
            self.current_connection.send_obj(res, server.INT_SIZE)
            self.shared_state.add_client()
        except Exception as e:
            print(f"Error adding player: {e}")

    def process_nr_x_quad_value(self):
        try:
            nr_x_quad = self.gamemech.get_nr_x()
            self.current_connection.send_int(nr_x_quad, server.INT_SIZE)
        except Exception as e:
            print(f"Error processing nr_x_quad_value: {e}")

    def process_nr_y_quad_value(self):
        try:
            nr_y_quad = self.gamemech.get_nr_y()
            self.current_connection.send_int(nr_y_quad, server.INT_SIZE)
        except Exception as e:
            print(f"Error processing nr_y_quad_value: {e}")

    def process_get_walls(self):
        try:
            walls = self.gamemech.get_walls()
            self.current_connection.send_obj(walls, server.INT_SIZE)
        except Exception as e:
            print(f"Error processing get_walls: {e}")

    def process_start_game(self):
        try:
            self.shared_state.start_game_sem().acquire()
            val = True
            self.current_connection.send_int(int(val), server.INT_SIZE)
        except Exception as e:
            print(f"Error processing start_game: {e}")

    def process_collect_item(self):
        try:
            player_id = self.current_connection.receive_int(server.INT_SIZE)
            collectible_id = self.current_connection.receive_int(server.INT_SIZE)
            self.gamemech.collect_item(player_id, collectible_id)
            self.shared_state.update_collectibles(self.gamemech.get_collectibles())
        except Exception as e:
            print(f"Error processing collect_item: {e}")

    def dispatch_request(self):
        try:
            request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
            print(request_type)
            keep_running = True
            last_request = False

            if request_type == server.STEP_OP:
                self.process_step()
            elif request_type == server.UPDATE_OP:
                self.process_update()
            elif request_type == server.QUADX_OP:
                self.process_nr_x_quad_value()
            elif request_type == server.QUADY_OP:
                self.process_nr_y_quad_value()
            elif request_type == server.PLAYER_OP:
                self.process_add_player()
            elif request_type == server.GET_OBJTS:
                self.process_objects()
            elif request_type == server.GET_WALLS_OP:
                self.process_get_walls()
            elif request_type == server.START_GAME:
                self.process_start_game()
            elif request_type == server.COLLECT_ITEM_OP:
                self.process_collect_item()
            elif request_type == server.BYE_OP:
                last_request = True
            elif request_type == server.STOP_SERVER_OP:
                last_request = True
                keep_running = False
            return keep_running, last_request
        except Exception as e:
            print(f"Error dispatching request: {e}")
            return False, True

    def run(self):
        last_request = False
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        logging.debug(f"Client {self.current_connection.get_address()} disconnected")

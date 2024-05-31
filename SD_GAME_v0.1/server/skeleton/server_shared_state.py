import threading
from server_impl.gamemech import GameMech
import server_impl

class ServerSharedState:
    def __init__(self, gamemech: GameMech):
        self._nr_connections = 0
        self._connections_lock = threading.Lock()
        self._start_game = False
        self._start_game_sem = threading.Semaphore(0)
        self._gamemech = gamemech
        self._collectibles = gamemech.get_collectibles()
        self._players = gamemech.get_players()  # Adicionar jogadores ao estado compartilhado

    def add_client(self):
        with self._connections_lock:
            self._nr_connections += 1
        if self._nr_connections == server_impl.NR_CLIENTS:
            with self._connections_lock:
                self._start_game = True
                for _ in range(self._nr_connections):
                    self._start_game_sem.release()

    def start_game_sem(self):
        return self._start_game_sem

    def gamemech(self):
        return self._gamemech

    def get_objects(self) -> dict:
        with self._connections_lock:
            players = self._gamemech.get_players()
            collectibles = self._collectibles
            res = {"players": players, "collectibles": collectibles}
        return res

    def update_collectibles(self, collectibles):
        with self._connections_lock:
            self._collectibles = collectibles

    def update_objects(self):
        with self._connections_lock:
            self._players = self._gamemech.get_players()
            self._collectibles = self._gamemech.get_collectibles()

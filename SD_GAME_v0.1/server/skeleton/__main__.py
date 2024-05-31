from server_impl.gamemech import GameMech
from skeleton.server_skeleton import GameServerSkeleton
from server_impl import NR_QUAD_X, NR_QUAD_Y

from server_shared_state import ServerSharedState

def main():
    gamemech = GameMech(NR_QUAD_X, NR_QUAD_Y)
    shared_state = ServerSharedState(gamemech)
    #skeleton =  GameServerSkeleton(gamemech)
    skeleton = GameServerSkeleton(shared_state)
    skeleton.run()

if __name__=="__main__":
    main()

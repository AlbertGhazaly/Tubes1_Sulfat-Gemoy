import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def countMoves(pos1: Position, pos2: Position):
    return abs(pos1.x-pos2.x) + abs(pos1.y-pos2.y)


class ClosestDiamond_Rafi(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.targetdiamond = None

    def next_move(self, board_bot: GameObject, board: Board):
        
        # for item in board.game_objects:
        #     # print(item)
        #     if item.type == "TeleportGameObject":
        #         print(item)

        # print(board_bot.position)

        props = board_bot.properties
        current_position = board_bot.position
        base = board_bot.properties.base

        # print(props)

        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            self.goal_position = base
        else:
            # Find Closest
            diamonds = board.diamonds
            teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]

            teleporter0_moves = countMoves(current_position, teleporters[0].position)
            teleporter1_moves = countMoves(current_position, teleporters[1].position)

            if teleporter0_moves < teleporter1_moves:
                teleport_exit_idx = 1
                entry_moves = teleporter0_moves
            else:
                teleport_exit_idx = 0
                entry_moves = teleporter1_moves

            self.goal_position = diamonds[0].position
            closest_diamond_via_teleport = diamonds[0].position

            curr_moves_via_teleport = 30

            for diamond in diamonds:

                if diamond.properties.points + props.diamonds > 5:
                    self.goal_position = base
                    continue

                curr_moves = countMoves(current_position, self.goal_position)
                new_moves = countMoves(current_position, diamond.position)

                new_moves_via_teleport = entry_moves + countMoves(teleporters[teleport_exit_idx].position,  diamond.position)

                if (new_moves < curr_moves):
                    self.goal_position = diamond.position

                if (new_moves_via_teleport < curr_moves_via_teleport):
                    curr_moves_via_teleport = new_moves_via_teleport
                    closest_diamond_via_teleport = diamond.position

            print("No teleporter moves: ", countMoves(current_position, self.goal_position))
            print("Teleporter moves: ", curr_moves_via_teleport)
            
            if countMoves(current_position, self.goal_position) > curr_moves_via_teleport:
                self.goal_position = closest_diamond_via_teleport

        # We are aiming for a specific position, calculate delta
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y
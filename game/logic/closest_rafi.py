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
        self.prioritymovement = "Horizontal"
        self.evade_portal = True

    def countDelta(self, current_position: Position, goal_position: Position, board: Board):

        teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        diamond_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]

        evade = []
        if self.evade_portal:
            evade.append(teleporters[0].position)
            evade.append(teleporters[1].position)
        evade.append(diamond_button[0].position)
 
        if current_position.x == goal_position.x:
            delta_x = 0
        else:
            delta_x = (goal_position.x - current_position.x) / abs(goal_position.x - current_position.x)
        if current_position.y == goal_position.y:
            delta_y = 0
        else:
            delta_y = (goal_position.y - current_position.y) / abs(goal_position.y - current_position.y)

        if delta_x != 0 and delta_y != 0:
            if self.prioritymovement == "Horizontal":
                delta_y = 0
            else:
                delta_x = 0

        if (Position(current_position.x + delta_x, current_position.y + delta_y) in evade):
            print("Awas menghindar!")
            if delta_x != 0:
                delta_x = 0
                if current_position.y == goal_position.y and current_position.y != 0:
                    delta_y = -1
                elif current_position.y == goal_position.y and current_position.y != 14:
                    delta_y = 1
                else:
                    delta_y = (goal_position.y - current_position.y) / abs(goal_position.y - current_position.y)
                self.prioritymovement = "Vertical"
            else:
                delta_y = 0
                if current_position.x == goal_position.x and current_position.y != 0:
                    delta_x = -1
                elif current_position.x == goal_position.x and current_position.y != 14:
                    delta_x = 1
                else:
                    delta_x = (goal_position.x - current_position.x) / abs(goal_position.x - current_position.x)
                self.prioritymovement = "Horizontal"

        return delta_x, delta_y

    def next_move(self, board_bot: GameObject, board: Board):
        
        # for item in board.game_objects:
        #     # print(item)
        #     if item.type == "TeleportGameObject":
        #         print(item)

        # print(board_bot.position)

        # bot props
        props = board_bot.properties

        # positions
        current_position = board_bot.position
        base = board_bot.properties.base

        # teleporters
        teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]

        teleporter0_moves = countMoves(current_position, teleporters[0].position)
        teleporter1_moves = countMoves(current_position, teleporters[1].position)

        if (teleporter0_moves < teleporter1_moves):
            teleport_enter = teleporters[0].position
            teleport_exit = teleporters[1].position

            moves_to_teleporter = teleporter0_moves
        else:
            teleport_enter = teleporters[1].position
            teleport_exit = teleporters[0].position

            moves_to_teleporter = teleporter1_moves


        # Analyze new state
        if props.diamonds == 5:

            if countMoves(current_position, base) > countMoves(current_position, teleport_enter) + countMoves(teleport_exit, base) and current_position != teleport_enter:
                self.goal_position = teleport_enter
            else:
                self.goal_position = base
        else:
            # Find Closest
            diamonds = board.diamonds
            
            closest_diamond = diamonds[0]
            closest_diamond_via_teleport = diamonds[0]

            curr_moves = countMoves(current_position, closest_diamond.position)
            curr_moves_via_teleport = moves_to_teleporter + countMoves(teleport_exit, closest_diamond_via_teleport.position)

            for diamond in diamonds:

                if diamond.properties.points + props.diamonds == 6:

                    return_home_flag = True

                else:
                    return_home_flag = False

                    new_moves = countMoves(current_position, diamond.position)
                    new_moves_via_teleport = moves_to_teleporter + countMoves(teleport_exit, diamond.position)

                    if (new_moves < curr_moves or closest_diamond.properties.points + props.diamonds == 6):
                        curr_moves = new_moves
                        closest_diamond = diamond

                    if (new_moves_via_teleport < curr_moves_via_teleport  or closest_diamond_via_teleport.properties.points + props.diamonds == 6):
                        curr_moves_via_teleport = new_moves_via_teleport
                        closest_diamond_via_teleport = diamond

            # print("No teleporter moves: ", countMoves(current_position, self.goal_position))
            # print("Teleporter moves: ", curr_moves_via_teleport)
            
            if not(return_home_flag):
                if (curr_moves_via_teleport < curr_moves and current_position != teleport_enter):
                    self.goal_position = teleport_enter
                    self.evade_portal = False
                else:
                    self.goal_position = closest_diamond.position
                    self.evade_portal = True
            else:
                if countMoves(current_position, base) < countMoves(current_position, teleport_enter) + countMoves(teleport_exit, base):
                    self.goal_position = base
                    self.evade_portal = True
                else:
                    self.goal_position = teleport_enter
                    self.evade_portal = False

        # We are aiming for a specific position, calculate delta
        # delta_x, delta_y = get_direction(
        #     current_position.x,
        #     current_position.y,
        #     self.goal_position.x,
        #     self.goal_position.y,
        # )
                    
        delta_x, delta_y = self.countDelta(current_position, self.goal_position, board)

        return delta_x, delta_y
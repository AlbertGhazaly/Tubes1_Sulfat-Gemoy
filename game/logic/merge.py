import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

def countMoves(pos1: Position, pos2: Position):
    return abs(pos1.x-pos2.x) + abs(pos1.y-pos2.y)

class Merge(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.targetdiamond = None

    def weghtcalcTel(self,curpos:Position,diampos:Position,weight,posbase:Position,closTel:Position,farTel:Position):
        distd = countMoves(curpos,diampos)
        distb = countMoves(diampos,closTel) + countMoves(farTel,posbase)
        return weight/distd -  distb/30
    
    def weghtcalc(self,curpos:Position,diampos:Position,weight,posbase:Position):
        distd = countMoves(curpos,diampos)
        distb = countMoves(diampos,posbase)
        return weight/distd - distb/30
    
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

                    print("Diamond full")


                    print(self.goal_position)

                else:
                    if (countMoves(teleporters[0].position,diamond.position) > countMoves(teleporters[1].position,diamond.position)):
                        teleporter_diamond_closest = teleporters[1].position
                        teleporter_diamond_farest = teleporters[0].position
                    else:
                        teleporter_diamond_closest = teleporters[0].position
                        teleporter_diamond_farest = teleporters[1].position
                
                    return_home_flag = False
                    weight = diamond.properties.points
                    maxw = closest_diamond.properties.points
                    new_moves = countMoves(current_position, diamond.position)
                    new_moves_via_teleport = moves_to_teleporter + countMoves(teleport_exit, diamond.position)
                    print(curr_moves)
                    print(new_moves)

                    if (self.weghtcalc(current_position,diamond.position,weight,base) > self.weghtcalc(current_position,closest_diamond.position,maxw,base)
                         or closest_diamond.properties.points + props.diamonds == 6):
                        curr_moves = new_moves
                        closest_diamond = diamond

                    if (self.weghtcalcTel(current_position,diamond.position,weight,base,teleporter_diamond_closest,teleporter_diamond_farest) <
                         self.weghtcalcTel(current_position,diamond.position,maxw,base,teleporter_diamond_closest,teleporter_diamond_farest)  or closest_diamond_via_teleport.properties.points + props.diamonds == 6):
                        curr_moves_via_teleport = new_moves_via_teleport
                        closest_diamond_via_teleport = diamond

            # print("No teleporter moves: ", countMoves(current_position, self.goal_position))
            # print("Teleporter moves: ", curr_moves_via_teleport)
            
            if not(return_home_flag):
                if (curr_moves_via_teleport < curr_moves and current_position != teleport_enter):
                    self.goal_position = teleport_enter
                else:
                    self.goal_position = closest_diamond.position
            else:
                if countMoves(current_position, base) < countMoves(current_position, teleport_enter) + countMoves(teleport_exit, base):
                    self.goal_position = base
                else:
                    self.goal_position = teleport_enter

            print(self.goal_position)

            

        # We are aiming for a specific position, calculate delta
        delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            self.goal_position.x,
            self.goal_position.y,
        )

        return delta_x, delta_y
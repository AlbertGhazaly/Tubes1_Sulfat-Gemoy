import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction




class Greed(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
    def distance(self, position1:Position, position2:Position):
        return abs(position1.y-position2.y) + abs(position1.x-position2.x)
    
    def weghtcalc(self,board_bot:GameObject,weight,pos:Position):
        distd = self.distance(board_bot.position,pos)
        distb = self.distance(board_bot.properties.base,pos)
        return weight/distd - 0.05 * distb
    def greed(self, board_bot:GameObject, board: Board):
        if (len(board.diamonds)> 0):
            max = board.diamonds[0]
            j = 1
            while (board_bot.properties.diamonds == 4 and max.properties.points == 2 and j<len(board.diamonds)):
                max = board.diamonds[j]
                j+=1

            for i in range(len(board.diamonds)):
                weight = board.diamonds[i].properties.points
                maxw = max.properties.points
                if (not (board_bot.properties.diamonds == 4 and weight == 2 and board_bot.position != board.diamonds[i].position) ):
                    if (self.weghtcalc(board_bot,maxw,max.position) < self.weghtcalc(board_bot,weight,board.diamonds[i].position)):
                        max = board.diamonds[i]

        return max.position

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = self.greed(board_bot,board)
            
        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            # Roam around
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        return delta_x, delta_y

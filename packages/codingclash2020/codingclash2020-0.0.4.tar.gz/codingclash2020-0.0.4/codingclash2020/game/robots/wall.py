from .. import constants as GameConstants
from ..robot_type import RobotType
from ..helpers import dist
from .robot import Robot

class Wall(Robot):
    def __init__(self, id, location, team):
        Robot.__init__(self, id,
                         location,
                         team, 
                         RobotType.WALL, 
                         GameConstants.WALL_HEALTH, 
                         -1)


    def run(self):
        Robot.run(self)

import random
from enum import Enum

class LandTypes(Enum):
    AA = 0
    INFANTRY = 1
    ARTILLERY = 2
    MECH_INFANTRY = 3
    TANK = 4

class SeaTypes(Enum):
    TRANSPORT = 0
    SUBMARINE = 1
    DESTROYER = 2
    CRUISER = 3
    AC_CARRIER = 4
    BATTLESHIP = 5

class AirTypes(Enum):
    FIGHTER = 0
    TACT_BOMBER = 1
    STRAT_BOMBER = 2

class PriorityTypes(Enum):
    ATTACK = 0
    DEFENSE = 1
    COST = 2

class Unit:
    def __init__(self, unit_type, cost, attack, defense, move, max_hits, opening_fire):
        self.name = unit_type.name
        self.priority = unit_type.value
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.move = move
        self.max_hits = max_hits
        self.hit_points = 0
        self.opening_fire = opening_fire # Boolean if unit allows for opening fire
        self.roll_value = 0

    def roll_attack(self):
        self.roll_value = random.randint(1,6)
        if self.roll_value <= self.attack:
            return 1
        else:
            return 0

    def roll_defense(self):
        self.roll_value = random.randint(1,6)
        if self.roll_value <= self.defense:
            return 1
        else:
            return 0

    def is_dead(self):
        # Kill units with sufficient hit-points, ignore 0-hit-point units (i.e. transports)
        if (self.hit_points >= self.max_hits) and (self.max_hits > 0):
            return True
        else:
            return False

    def assign_hit(self):
        if not self.is_dead():
            self.hit_points += 1
            return True
        else:
            return False

# Declare instance of each unit types
unit_infantry = Unit(LandTypes.INFANTRY, 3, 1, 2, 1, 1, False)
unit_artillery = Unit(LandTypes.ARTILLERY, 4, 2, 2, 1, 1, False)
unit_mech_infantry = Unit(LandTypes.MECH_INFANTRY, 4, 1, 2, 2, 1, False)
unit_tank = Unit(LandTypes.TANK, 6, 3, 3, 2, 1, False)
unit_aa = Unit(LandTypes.AA, 5, 0, 0, 1, 1, True)
unit_fighter = Unit(AirTypes.FIGHTER, 10, 3, 4, 4, 1, False)
unit_tact_bomber = Unit(AirTypes.TACT_BOMBER, 11, 3, 3, 4, 1, False)
unit_strat_bomber = Unit(AirTypes.STRAT_BOMBER, 12, 4, 1, 6, 1, False)
unit_battleship = Unit(SeaTypes.BATTLESHIP, 20, 4, 4, 2, 2, True)
unit_ac_carrier = Unit(SeaTypes.AC_CARRIER, 16, 0, 2, 2, 2, False)
unit_cruiser = Unit(SeaTypes.CRUISER, 12, 3, 3, 2, 1, True)
unit_destroyer = Unit(SeaTypes.DESTROYER, 8, 2, 2, 2, 1, False)
unit_submarine = Unit(SeaTypes.SUBMARINE, 6, 2, 1, 2, 1, True)
unit_transport = Unit(SeaTypes.TRANSPORT, 7, 0, 0, 2, 0, False)

unit_list = [unit_infantry, unit_artillery, unit_mech_infantry, unit_tank, unit_aa,
             unit_fighter, unit_tact_bomber, unit_strat_bomber,
             unit_battleship, unit_ac_carrier, unit_cruiser,
             unit_destroyer, unit_submarine, unit_transport]